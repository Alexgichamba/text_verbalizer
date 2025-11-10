"""
Base normalizer class for text normalization.
All language-specific normalizers should inherit from this class.
"""

import re
import warnings
from abc import ABC, abstractmethod


class BaseNormalizer(ABC):
    """
    Abstract base class for text normalization.
    
    All language-specific normalizers must implement the abstract methods.
    """
    
    def __init__(self):
        """Initialize the normalizer with language-specific patterns."""
        self.patterns = self._get_patterns()
    
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
                return self.verbalize_number(match.group())
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
        
        Args:
            text (str): Input text
            
        Returns:
            str: Fully normalized text
        """
        # Process currency first (contains numbers)
        text = self.normalize_currency(text)
        
        # Then dates (contains numbers)
        text = self.normalize_dates(text)
        
        # Then time (contains numbers)
        text = self.normalize_time(text)
        
        # Finally standalone numbers
        text = self.normalize_numbers(text)
        
        return text