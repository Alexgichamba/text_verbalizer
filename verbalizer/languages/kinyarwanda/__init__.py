"""
Kinyarwanda text verbalizer.

Main verbalizer class for Kinyarwanda language.
"""

from ...base import BaseNormalizer
from .config import PATTERNS
from .number import digit_string as digit_string_rw
from .number import verbalize_number as verbalize_number_rw
from .currency import verbalize_currency as verbalize_currency_rw
from .time import verbalize_time as verbalize_time_rw
from .date import parse_and_verbalize_date as verbalize_date_rw


class KinyarwandaVerbalizer(BaseNormalizer):
    """
    Text verbalizer for Kinyarwanda language.

    Handles verbalization of:
    - Numbers (integers and decimals, with noun-class concord on multipliers)
    - Currency (RWF, FRW, USD, EUR, KES, UGX, TZS)
    - Time (12h and 24h formats)
    - Dates (DD/MM/YYYY format)
    """

    def __init__(self, read_digits="auto", digit_threshold=None,
                 protect_brackets=True):
        """Initialize Kinyarwanda verbalizer.

        See :class:`~verbalizer.base.BaseNormalizer` for ``read_digits``,
        ``digit_threshold`` and ``protect_brackets``.
        """
        super().__init__(
            read_digits=read_digits,
            digit_threshold=digit_threshold,
            protect_brackets=protect_brackets,
        )

    def _get_patterns(self):
        """Return Kinyarwanda-specific regex patterns."""
        return PATTERNS

    def verbalize_number(self, number_str):
        """
        Convert a number string to Kinyarwanda words.

        Args:
            number_str (str): String representation of a number

        Returns:
            str: Verbalized number in Kinyarwanda
        """
        return verbalize_number_rw(number_str)

    def verbalize_digits(self, number_str):
        """
        Read a number one digit at a time (phone numbers, IDs).

        Args:
            number_str (str): String of digits

        Returns:
            str: Digits read out individually
        """
        return digit_string_rw(number_str)

    def verbalize_currency(self, match):
        """
        Convert a currency amount to Kinyarwanda words.

        Args:
            match: Regex match object with groups (currency_code, amount)

        Returns:
            str: Verbalized currency in Kinyarwanda
        """
        currency_code = match.group(1).upper()
        amount = match.group(2)
        return verbalize_currency_rw(currency_code, amount)

    def verbalize_time(self, match):
        """
        Convert a time to Kinyarwanda words.

        Args:
            match: Regex match object with time components

        Returns:
            str: Verbalized time in Kinyarwanda
        """
        hours = match.group(1)
        minutes = match.group(2)
        seconds = match.group(3) if match.group(3) else ""
        period = match.group(4) if match.group(4) else ""

        time_str = "%s:%s" % (hours, minutes)
        if seconds:
            time_str += ":%s" % seconds
        if period:
            time_str += " %s" % period

        return verbalize_time_rw(time_str)

    def verbalize_date(self, match):
        """
        Convert a date to Kinyarwanda words.

        Args:
            match: Regex match object with groups (day, month, year)

        Returns:
            str: Verbalized date in Kinyarwanda
        """
        date_str = match.group()
        return verbalize_date_rw(date_str)
