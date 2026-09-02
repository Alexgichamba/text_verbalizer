# verbalizer/languages/swahili/number.py

"""
Swahili number verbalization.

Handles conversion of numbers to Swahili words.
"""

# Basic digits 0-9
ONES = {
    0: "sifuri",
    1: "moja",
    2: "mbili",
    3: "tatu",
    4: "nne",
    5: "tano",
    6: "sita",
    7: "saba",
    8: "nane",
    9: "tisa",
}

# Tens 10-90
TENS = {
    10: "kumi",
    20: "ishirini",
    30: "thelathini",
    40: "arobaini",
    50: "hamsini",
    60: "sitini",
    70: "sabini",
    80: "themanini",
    90: "tisini",
}

# Scale words
HUNDRED = "mia"
THOUSAND = "elfu"
MILLION = "milioni"
BILLION = "bilioni"


def _join_components(parts):
    """Join additive components with Swahili ``na``.

    Swahili places ``na`` before the *final* component only; the earlier
    components are simply juxtaposed. So 325 is "mia tatu ishirini na tano",
    not "mia tatu na ishirini na tano".
    """
    if len(parts) == 1:
        return parts[0]
    return " ".join(parts[:-1]) + " na " + parts[-1]


def _components(n):
    """Decompose a non-negative integer into its additive spoken components.

    Each component is a self-contained group ("elfu mbili", "mia tatu",
    "arobaini", "tano"); the caller joins them with :func:`_join_components`.
    """
    if n == 0:
        return [ONES[0]]

    for scale_value, scale_word in (
        (1_000_000_000, BILLION),
        (1_000_000, MILLION),
        (1000, THOUSAND),
        (100, HUNDRED),
    ):
        if n >= scale_value:
            multiplier, remainder = divmod(n, scale_value)
            # The multiplier is a number in its own right and takes its own
            # internal "na" (15000 -> "elfu kumi na tano").
            parts = ["%s %s" % (scale_word, _join_components(_components(multiplier)))]
            if remainder:
                parts.extend(_components(remainder))
            return parts

    if n >= 10:
        tens_digit, ones_digit = divmod(n, 10)
        parts = [TENS[tens_digit * 10]]
        if ones_digit:
            parts.append(ONES[ones_digit])
        return parts

    return [ONES[n]]


def number_to_words(n):
    """
    Convert an integer to Swahili words.

    Args:
        n (int): Number to convert (0 to 999,999,999,999)

    Returns:
        str: Swahili word representation
    """
    if n < 0:
        return "hasi " + number_to_words(-n)

    return _join_components(_components(n))


def verbalize_number(number_str):
    """
    Convert a number string to Swahili words.
    Handles integers and decimals.
    
    Args:
        number_str (str): String representation of a number
        
    Returns:
        str: Verbalized number in Swahili
    """
    number_str = number_str.strip()
    
    # Handle decimal numbers
    if '.' in number_str:
        integer_part, decimal_part = number_str.split('.')
        
        result = number_to_words(int(integer_part))
        result += " nukta"
        
        # Read each decimal digit separately
        for digit in decimal_part:
            result += f" {ONES[int(digit)]}"
        
        return result
    
    # Handle integers
    return number_to_words(int(number_str))