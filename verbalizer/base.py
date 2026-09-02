"""
Base verbalizer class for text normalization.
All language-specific normalizers should inherit from this class.
"""

import re
import warnings
from abc import ABC, abstractmethod


#: Bracketed spans are the inline control syntax used by TTS front-ends
#: (e.g. OmniVoice's ``[laughter]`` non-verbal tags and ``[B EY1 S]``
#: pronunciation overrides). They are markup, not speech, so they are held
#: out of normalization and re-inserted verbatim -- otherwise a stress digit
#: or a bracketed count would be read aloud as a number.
BRACKET_SPAN_RE = re.compile(r'\[[^\[\]]*\]')


class BaseNormalizer(ABC):
    """
    Abstract base class for text normalization.
    
    All language-specific normalizers must implement the abstract methods.
    """
    
    #: Values accepted by the ``read_digits`` option.
    READ_DIGITS_MODES = ("auto", "always", "never")

    def __init__(self, read_digits="auto", digit_threshold=None,
                 protect_brackets=True):
        """Initialize the verbalizer with language-specific patterns.

        Args:
            read_digits (str): How to read a bare run of digits.

                * ``"auto"`` (default) -- read a token digit by digit only
                  when it has a leading zero, which is an unambiguous signal
                  that it is an identifier (a phone number, an account or ID
                  number) rather than a quantity. Everything else is read as
                  a cardinal.
                * ``"always"`` -- read every numeric token digit by digit.
                * ``"never"`` -- read every numeric token as a cardinal, even
                  one with a leading zero.

            digit_threshold (int, optional): Under ``"auto"``, also read a
                token digit by digit once it has at least this many digits.
                Off by default, because the cut-off is corpus-specific: a
                phone number written without its leading zero (``250788123456``)
                wants it, but a genuine large quantity does not. 7 is a
                reasonable setting for text that contains phone numbers.

            protect_brackets (bool): Whether to pass bracketed spans through
                :meth:`normalize` untouched. Defaults to ``True``. See
                :data:`BRACKET_SPAN_RE`.
        """
        if read_digits not in self.READ_DIGITS_MODES:
            raise ValueError(
                "read_digits must be one of %r, got %r"
                % (self.READ_DIGITS_MODES, read_digits)
            )
        self.read_digits = read_digits
        self.digit_threshold = digit_threshold
        self.protect_brackets = protect_brackets
        self.patterns = self._get_patterns()

    def should_read_digits(self, number_str):
        """Return whether ``number_str`` should be read digit by digit."""
        if self.read_digits == "never":
            return False
        if self.read_digits == "always":
            return True

        # "auto": a leading zero marks an identifier, not a quantity.
        digits = number_str.lstrip("+-")
        if len(digits) > 1 and digits.startswith("0") and not digits.startswith("0."):
            return True
        if self.digit_threshold is not None:
            return sum(c.isdigit() for c in digits) >= self.digit_threshold
        return False

    def verbalize_digits(self, number_str):
        """Read ``number_str`` one digit at a time.

        Subclasses override this with their own digit names. The default
        keeps older subclasses working by falling back to the cardinal
        reading.
        """
        return self.verbalize_number(number_str)
    
    @abstractmethod
    def _get_patterns(self):
        """
        Return regex patterns for detecting numbers, currency, time, and dates.
        
        Returns:
            dict: Dictionary of compiled regex patterns
        """
        pass
    
    @abstractmethod
    def verbalize_number(self, number_str):
        """
        Convert a number string to its verbal form.
        
        Args:
            number_str (str): String representation of a number
            
        Returns:
            str: Verbalized number
        """
        pass
    
    @abstractmethod
    def verbalize_currency(self, match):
        """
        Convert a currency amount to its verbal form.
        
        Args:
            match: Regex match object containing currency information
            
        Returns:
            str: Verbalized currency
        """
        pass
    
    @abstractmethod
    def verbalize_time(self, match):
        """
        Convert a time to its verbal form.
        
        Args:
            match: Regex match object containing time information
            
        Returns:
            str: Verbalized time
        """
        pass
    
    @abstractmethod
    def verbalize_date(self, match):
        """
        Convert a date to its verbal form.
        
        Args:
            match: Regex match object containing date information
            
        Returns:
            str: Verbalized date
        """
        pass
    
    def normalize_numbers(self, text):
        """
        Normalize all numbers in text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized numbers
        """
        def replace_number(match):
            try:
                token = match.group()
                if self.should_read_digits(token):
                    return self.verbalize_digits(token)
                return self.verbalize_number(token)
            except Exception as e:
                warnings.warn(f"Failed to normalize number '{match.group()}': {str(e)}")
                return match.group()
        
        return self.patterns['number'].sub(replace_number, text)
    
    def normalize_currency(self, text):
        """
        Normalize all currency amounts in text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized currency
        """
        def replace_currency(match):
            try:
                return self.verbalize_currency(match)
            except Exception as e:
                warnings.warn(f"Failed to normalize currency '{match.group()}': {str(e)}")
                return match.group()
        
        return self.patterns['currency'].sub(replace_currency, text)
    
    def normalize_time(self, text):
        """
        Normalize all time expressions in text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized time
        """
        def replace_time(match):
            try:
                return self.verbalize_time(match)
            except Exception as e:
                warnings.warn(f"Failed to normalize time '{match.group()}': {str(e)}")
                return match.group()
        
        return self.patterns['time'].sub(replace_time, text)
    
    def normalize_dates(self, text):
        """
        Normalize all dates in text.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Text with normalized dates
        """
        def replace_date(match):
            try:
                return self.verbalize_date(match)
            except Exception as e:
                warnings.warn(f"Failed to normalize date '{match.group()}': {str(e)}")
                return match.group()
        
        return self.patterns['date'].sub(replace_date, text)
    
    def normalize(self, text):
        """
        Apply all normalizations to text.
        
        The order is: currency -> dates -> time -> numbers
        This prevents double-normalization of numbers in currency/time/date expressions.
        
        Bracketed inline control spans are preserved verbatim unless the
        verbalizer was constructed with ``protect_brackets=False``.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Fully normalized text
        """
        if self.protect_brackets and '[' in text:
            out = []
            last = 0
            for match in BRACKET_SPAN_RE.finditer(text):
                start, end = match.span()
                out.append(self._normalize_unprotected(text[last:start]))
                out.append(match.group())  # control span, verbatim
                last = end
            out.append(self._normalize_unprotected(text[last:]))
            return ''.join(out)
        return self._normalize_unprotected(text)
    
    def _normalize_unprotected(self, text):
        """Run every normalization stage over a span with no control syntax."""
        # Process currency first (contains numbers)
        text = self.normalize_currency(text)
        
        # Then dates (contains numbers)
        text = self.normalize_dates(text)
        
        # Then time (contains numbers)
        text = self.normalize_time(text)
        
        # Finally standalone numbers
        text = self.normalize_numbers(text)
        
        return text