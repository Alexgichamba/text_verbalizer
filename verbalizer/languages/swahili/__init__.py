"""
Swahili text normalizer.

Main normalizer class for Swahili language.
"""

from ...base import BaseNormalizer
from .config import PATTERNS
from .number import verbalize_number as verbalize_number_sw
from .currency import verbalize_currency as verbalize_currency_sw
from .time import verbalize_time as verbalize_time_sw
from .date import parse_and_verbalize_date as verbalize_date_sw


class SwahiliNormalizer(BaseNormalizer):
    """
    Text normalizer for Swahili language.
    
    Handles verbalization of:
    - Numbers (integers and decimals)
    - Currency (KES, TZS, NGN, RWF)
    - Time (12h and 24h formats)
    - Dates (DD/MM/YYYY format)
    """
    
    def __init__(self):
        """Initialize Swahili normalizer."""
        super().__init__()
    
    def _get_patterns(self):
        """Return Swahili-specific regex patterns."""
        return PATTERNS
    
    def verbalize_number(self, number_str):
        """
        Convert a number string to Swahili words.
        
        Args:
            number_str (str): String representation of a number
            
        Returns:
            str: Verbalized number in Swahili
        """
        return verbalize_number_sw(number_str)
    
    def verbalize_currency(self, match):
        """
        Convert a currency amount to Swahili words.
        
        Args:
            match: Regex match object with groups (currency_code, amount)
            
        Returns:
            str: Verbalized currency in Swahili
        """
        currency_code = match.group(1).upper()
        amount = match.group(2)
        return verbalize_currency_sw(currency_code, amount)
    
    def verbalize_time(self, match):
        """
        Convert a time to Swahili words.
        
        Args:
            match: Regex match object with time components
            
        Returns:
            str: Verbalized time in Swahili
        """
        # Reconstruct the time string from match groups
        hours = match.group(1)
        minutes = match.group(2)
        seconds = match.group(3) if match.group(3) else ""
        period = match.group(4) if match.group(4) else ""
        
        time_str = f"{hours}:{minutes}"
        if seconds:
            time_str += f":{seconds}"
        if period:
            time_str += f" {period}"
        
        return verbalize_time_sw(time_str)
    
    def verbalize_date(self, match):
        """
        Convert a date to Swahili words.
        
        Args:
            match: Regex match object with groups (day, month, year)
            
        Returns:
            str: Verbalized date in Swahili
        """
        date_str = match.group()
        return verbalize_date_sw(date_str)