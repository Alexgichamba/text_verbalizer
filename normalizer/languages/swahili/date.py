# normalizer/languages/swahili/date.py

"""
Swahili date verbalization.

Handles conversion of dates to Swahili words.
Format: DD/MM/YYYY
"""

from .numbers import number_to_words


# Month names in Swahili
MONTHS = {
    1: "Januari",
    2: "Februari",
    3: "Machi",
    4: "Aprili",
    5: "Mei",
    6: "Juni",
    7: "Julai",
    8: "Agosti",
    9: "Septemba",
    10: "Oktoba",
    11: "Novemba",
    12: "Desemba",
}


def verbalize_date(day, month, year):
    """
    Convert a date to Swahili words.
    
    Args:
        day (int): Day of month (1-31)
        month (int): Month (1-12)
        year (int): Year
        
    Returns:
        str: Verbalized date in Swahili
    """
    # Day
    day_words = number_to_words(day)
    
    # Month name
    month_name = MONTHS.get(month, f"mwezi {number_to_words(month)}")
    
    # Year
    year_words = number_to_words(year)
    
    # Format: "tarehe [day] mwezi wa [month] mwaka [year]"
    return f"tarehe {day_words} mwezi wa {month_name} mwaka {year_words}"


def parse_and_verbalize_date(date_str):
    """
    Parse a date string and convert to Swahili words.
    Expected format: DD/MM/YYYY
    
    Args:
        date_str (str): Date string in DD/MM/YYYY format
        
    Returns:
        str: Verbalized date in Swahili
    """
    parts = date_str.strip().split('/')
    
    if len(parts) != 3:
        raise ValueError(f"Invalid date format: {date_str}. Expected DD/MM/YYYY")
    
    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])
    
    # Basic validation
    if not (1 <= day <= 31):
        raise ValueError(f"Invalid day: {day}")
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}")
    if year < 0:
        raise ValueError(f"Invalid year: {year}")
    
    return verbalize_date(day, month, year)