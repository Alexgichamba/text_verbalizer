# verbalizer/languages/swahili/config.py

"""
Swahili configuration and regex patterns.
"""

import re


# Regex patterns for detection
PATTERNS = {
    # Currency: Matches KES 1000, TZS 50.25, etc.
    # Must match before plain numbers to avoid double normalization
    'currency': re.compile(
        r'\b(KES|TZS|NGN|RWF)\s*(\d+(?:\.\d{1,2})?)\b',
        re.IGNORECASE
    ),
    
    # Date: DD/MM/YYYY format
    'date': re.compile(
        r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b'
    ),
    
    # Time: Matches both 12h (14:30, 2:30 PM) and 24h (14:30:45) formats
    'time': re.compile(
        r'\b(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM|am|pm)?\b'
    ),
    
    # Plain numbers (integers and decimals)
    # This should be matched last to avoid conflict with currency/time/date
    'number': re.compile(
        r'\b\d+(?:\.\d+)?\b'
    ),
}


# Currency codes supported
SUPPORTED_CURRENCIES = ['KES', 'TZS', 'NGN', 'RWF']