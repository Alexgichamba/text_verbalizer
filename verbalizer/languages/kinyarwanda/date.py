# verbalizer/languages/kinyarwanda/date.py

"""
Kinyarwanda date verbalization.

Handles conversion of dates to Kinyarwanda words.
Format: DD/MM/YYYY
"""

from .number import _VOWELS, number_to_words


# Month names in Kinyarwanda
MONTHS = {
    1: "Mutarama",
    2: "Gashyantare",
    3: "Werurwe",
    4: "Mata",
    5: "Gicurasi",
    6: "Kamena",
    7: "Nyakanga",
    8: "Kanama",
    9: "Nzeri",
    10: "Ukwakira",
    11: "Ugushyingo",
    12: "Ukuboza",
}


def verbalize_date(day, month, year):
    """
    Convert a date to Kinyarwanda words.

    Args:
        day (int): Day of month (1-31)
        month (int): Month (1-12)
        year (int): Year

    Returns:
        str: Verbalized date in Kinyarwanda
    """
    day_words = number_to_words(day)
    month_name = MONTHS.get(month, "ukwezi kwa %s" % number_to_words(month))
    year_words = number_to_words(year)

    # "wa" elides its vowel before a vowel-initial year, exactly as "na"
    # does: "mu mwaka w'ibihumbi bibiri", not "mu mwaka wa ibihumbi bibiri".
    if year_words[:1].lower() in _VOWELS:
        year_phrase = "mu mwaka w'%s" % year_words
    else:
        year_phrase = "mu mwaka wa %s" % year_words

    # Format: "tariki ya [day] [month] mu mwaka wa [year]"
    return "tariki ya %s %s %s" % (day_words, month_name, year_phrase)


def parse_and_verbalize_date(date_str):
    """
    Parse a date string and convert to Kinyarwanda words.
    Expected format: DD/MM/YYYY

    Args:
        date_str (str): Date string in DD/MM/YYYY format

    Returns:
        str: Verbalized date in Kinyarwanda
    """
    parts = date_str.strip().split('/')

    if len(parts) != 3:
        raise ValueError("Invalid date format: %s. Expected DD/MM/YYYY" % date_str)

    day = int(parts[0])
    month = int(parts[1])
    year = int(parts[2])

    if not (1 <= day <= 31):
        raise ValueError("Invalid day: %s" % day)
    if not (1 <= month <= 12):
        raise ValueError("Invalid month: %s" % month)
    if year < 0:
        raise ValueError("Invalid year: %s" % year)

    return verbalize_date(day, month, year)
