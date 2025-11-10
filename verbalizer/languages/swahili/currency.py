# verbalizer/languages/swahili/currency.py

"""
Swahili currency verbalization.

Handles conversion of currency amounts to Swahili words.
"""

from .number import number_to_words


# Currency definitions
CURRENCIES = {
    'KES': {
        'name': 'shilingi',
        'singular': 'shilingi',
        'plural': 'shilingi',
        'subunit': 'senti',
        'symbol': 'KES'
    },
    'TZS': {
        'name': 'shilingi',
        'singular': 'shilingi',
        'plural': 'shilingi',
        'subunit': 'senti',
        'symbol': 'TZS'
    },
    'NGN': {
        'name': 'naira',
        'singular': 'naira',
        'plural': 'naira',
        'subunit': 'kobo',
        'symbol': 'NGN'
    },
    'RWF': {
        'name': 'faranga',
        'singular': 'faranga',
        'plural': 'faranga',
        'subunit': 'santim',
        'symbol': 'RWF'
    },
}


def verbalize_currency(currency_code, amount_str):
    """
    Convert a currency amount to Swahili words.
    
    Args:
        currency_code (str): Currency code (KES, TZS, NGN, RWF)
        amount_str (str): Amount as string (can include decimals)
        
    Returns:
        str: Verbalized currency amount
    """
    if currency_code not in CURRENCIES:
        return f"{currency_code} {amount_str}"
    
    currency = CURRENCIES[currency_code]
    
    # Parse amount
    if '.' in amount_str:
        main_amount, sub_amount = amount_str.split('.')
        main_amount = int(main_amount)
        sub_amount = int(sub_amount)
    else:
        main_amount = int(amount_str)
        sub_amount = 0
    
    # Verbalize main amount
    result = f"{currency['name']} {number_to_words(main_amount)}"
    
    # Verbalize subunit if present
    if sub_amount > 0:
        result += f" na {currency['subunit']} {number_to_words(sub_amount)}"
    
    return result