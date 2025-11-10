# normalizer/languages/swahili/number.py

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


def number_to_words(n):
    """
    Convert an integer to Swahili words.
    
    Args:
        n (int): Number to convert (0 to 999,999,999,999)
        
    Returns:
        str: Swahili word representation
    """
    if n == 0:
        return ONES[0]
    
    if n < 0:
        return "hasi " + number_to_words(-n)
    
    # Handle billions
    if n >= 1_000_000_000:
        billions = n // 1_000_000_000
        remainder = n % 1_000_000_000
        
        if billions == 1:
            result = f"{BILLION} moja"
        else:
            result = f"{BILLION} {number_to_words(billions)}"
        
        if remainder > 0:
            result += f" na {number_to_words(remainder)}"
        return result
    
    # Handle millions
    if n >= 1_000_000:
        millions = n // 1_000_000
        remainder = n % 1_000_000
        
        if millions == 1:
            result = f"{MILLION} moja"
        else:
            result = f"{MILLION} {number_to_words(millions)}"
        
        if remainder > 0:
            result += f" na {number_to_words(remainder)}"
        return result
    
    # Handle thousands
    if n >= 1000:
        thousands = n // 1000
        remainder = n % 1000
        
        if thousands == 1:
            result = f"{THOUSAND} moja"
        else:
            result = f"{THOUSAND} {number_to_words(thousands)}"
        
        if remainder > 0:
            result += f" na {number_to_words(remainder)}"
        return result
    
    # Handle hundreds
    if n >= 100:
        hundreds = n // 100
        remainder = n % 100
        
        if hundreds == 1:
            result = f"{HUNDRED} moja"
        else:
            result = f"{HUNDRED} {number_to_words(hundreds)}"
        
        if remainder > 0:
            result += f" na {number_to_words(remainder)}"
        return result
    
    # Handle 10-99
    if n >= 10:
        tens_digit = (n // 10) * 10
        ones_digit = n % 10
        
        if ones_digit == 0:
            return TENS[tens_digit]
        else:
            return f"{TENS[tens_digit]} na {ONES[ones_digit]}"
    
    # Handle 1-9
    return ONES[n]


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