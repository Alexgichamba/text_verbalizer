# verbalizer/languages/kinyarwanda/time.py

"""
Kinyarwanda time verbalization.

Handles conversion of time expressions to Kinyarwanda words.

Kinyarwanda traditionally counts hours from sunrise (7 AM = "saa moya"), but
as in the Swahili module we use standard clock hours with the "saa" prefix,
which is what a TTS front-end reading a digital timestamp wants.

"saa" is a class 9/10 noun, so the hour takes the N- concord series
("saa imwe", "saa ebyiri", "saa eshatu"). Minutes ("iminota", class 4) and
seconds ("amasegonda", class 6) take their own series, but above ten the
counting forms are used, which is the common spoken pattern.
"""

from .number import CONCORD_N, number_to_words, _na


MINUTES_WORD = "iminota"
SECONDS_WORD = "amasegonda"
MORNING = "mu gitondo"
EVENING = "nimugoroba"


def _hour_words(hours):
    """Spell an hour with the class 9/10 concord that ``saa`` governs."""
    if hours in CONCORD_N:
        return CONCORD_N[hours]
    return number_to_words(hours)


def verbalize_time_24h(hours, minutes, seconds=None):
    """
    Convert 24-hour time to Kinyarwanda words.

    Args:
        hours (int): Hour (0-23)
        minutes (int): Minutes (0-59)
        seconds (int, optional): Seconds (0-59)

    Returns:
        str: Verbalized time in Kinyarwanda
    """
    result = "saa %s" % _hour_words(hours)

    if minutes > 0:
        result += " " + _na("%s %s" % (MINUTES_WORD, number_to_words(minutes)))

    if seconds is not None and seconds > 0:
        result += " " + _na("%s %s" % (SECONDS_WORD, number_to_words(seconds)))

    return result


def verbalize_time_12h(hours, minutes, period, seconds=None):
    """
    Convert 12-hour time to Kinyarwanda words.

    Args:
        hours (int): Hour (1-12)
        minutes (int): Minutes (0-59)
        period (str): 'AM' or 'PM'
        seconds (int, optional): Seconds (0-59)

    Returns:
        str: Verbalized time in Kinyarwanda
    """
    # Convert to 24h for consistency
    if period.upper() == 'PM' and hours != 12:
        hours_24 = hours + 12
    elif period.upper() == 'AM' and hours == 12:
        hours_24 = 0
    else:
        hours_24 = hours

    result = verbalize_time_24h(hours_24, minutes, seconds)

    if period.upper() == 'AM':
        result += " " + MORNING
    else:
        result += " " + EVENING

    return result


def verbalize_time(time_str):
    """
    Convert a time string to Kinyarwanda words.
    Handles both 12-hour and 24-hour formats.

    Args:
        time_str (str): Time string (e.g., "14:30", "2:30 PM", "14:30:45")

    Returns:
        str: Verbalized time in Kinyarwanda
    """
    time_str = time_str.strip()

    # Check for AM/PM (12-hour format)
    period = None
    if time_str.upper().endswith('AM') or time_str.upper().endswith('PM'):
        period = time_str[-2:].upper()
        time_str = time_str[:-2].strip()

    parts = time_str.split(':')
    hours = int(parts[0])
    minutes = int(parts[1]) if len(parts) > 1 else 0
    seconds = int(parts[2]) if len(parts) > 2 else None

    if period:
        return verbalize_time_12h(hours, minutes, period, seconds)
    return verbalize_time_24h(hours, minutes, seconds)
