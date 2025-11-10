# verbalizer/languages/swahili/time.py

"""
Swahili time verbalization.

Handles conversion of time expressions to Swahili words.
In Swahili, time is counted from sunrise (7 AM = saa moja, 1 PM = saa saba, etc.)
For simplicity and clarity in TTS, we'll use the standard clock hours with 'saa' prefix.
"""

from .number import number_to_words


def verbalize_time_24h(hours, minutes, seconds=None):
    """
    Convert 24-hour time to Swahili words.
    
    Args:
        hours (int): Hour (0-23)
        minutes (int): Minutes (0-59)
        seconds (int, optional): Seconds (0-59)
        
    Returns:
        str: Verbalized time in Swahili
    """
    result = f"saa {number_to_words(hours)}"
    
    if minutes > 0:
        result += f" na dakika {number_to_words(minutes)}"
    
    if seconds is not None and seconds > 0:
        result += f" na sekunde {number_to_words(seconds)}"
    
    return result


def verbalize_time_12h(hours, minutes, period, seconds=None):
    """
    Convert 12-hour time to Swahili words.
    
    Args:
        hours (int): Hour (1-12)
        minutes (int): Minutes (0-59)
        period (str): 'AM' or 'PM'
        seconds (int, optional): Seconds (0-59)
        
    Returns:
        str: Verbalized time in Swahili
    """
    # Convert to 24h for consistency
    if period.upper() == 'PM' and hours != 12:
        hours_24 = hours + 12
    elif period.upper() == 'AM' and hours == 12:
        hours_24 = 0
    else:
        hours_24 = hours
    
    result = f"saa {number_to_words(hours_24)}"
    
    if minutes > 0:
        result += f" na dakika {number_to_words(minutes)}"
    
    if seconds is not None and seconds > 0:
        result += f" na sekunde {number_to_words(seconds)}"
    
    # Optionally add period indicator
    if period.upper() == 'AM':
        result += " asubuhi"
    else:
        result += " jioni"
    
    return result


def verbalize_time(time_str):
    """
    Convert a time string to Swahili words.
    Handles both 12-hour and 24-hour formats.
    
    Args:
        time_str (str): Time string (e.g., "14:30", "2:30 PM", "14:30:45")
        
    Returns:
        str: Verbalized time in Swahili
    """
    time_str = time_str.strip()
    
    # Check for AM/PM (12-hour format)
    period = None
    if time_str.upper().endswith('AM') or time_str.upper().endswith('PM'):
        period = time_str[-2:].upper()
        time_str = time_str[:-2].strip()
    
    # Split time components
    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    seconds = int(parts[2]) if len(parts) > 2 else None
    
    # Verbalize based on format
    if period:
        return verbalize_time_12h(hours, minutes, period, seconds)
    else:
        return verbalize_time_24h(hours, minutes, seconds)