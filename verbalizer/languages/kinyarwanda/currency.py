# verbalizer/languages/kinyarwanda/currency.py

"""
Kinyarwanda currency verbalization.

Handles conversion of currency amounts to Kinyarwanda words.
"""

from .number import number_to_words, _na


# Currency definitions.
# ``name`` is a class 6 plural noun ("amafaranga", "amadolari"), which is why
# the amount simply follows it without further agreement.
CURRENCIES = {
    'RWF': {
        'name': "amafaranga y'u Rwanda",
        'subunit': 'santimu',
        'symbol': 'RWF',
    },
    'FRW': {
        'name': "amafaranga y'u Rwanda",
        'subunit': 'santimu',
        'symbol': 'FRW',
    },
    'USD': {
        'name': 'amadolari',
        'subunit': 'santimu',
        'symbol': 'USD',
    },
    'EUR': {
        'name': 'amayero',
        'subunit': 'santimu',
        'symbol': 'EUR',
    },
    'KES': {
        'name': 'amashilingi ya Kenya',
        'subunit': 'santimu',
        'symbol': 'KES',
    },
    'UGX': {
        'name': 'amashilingi ya Uganda',
        'subunit': 'santimu',
        'symbol': 'UGX',
    },
    'TZS': {
        'name': 'amashilingi ya Tanzaniya',
        'subunit': 'santimu',
        'symbol': 'TZS',
    },
}


def verbalize_currency(currency_code, amount_str):
    """
    Convert a currency amount to Kinyarwanda words.

    Args:
        currency_code (str): Currency code (RWF, FRW, USD, EUR, KES, UGX, TZS)
        amount_str (str): Amount as string (can include decimals)

    Returns:
        str: Verbalized currency amount
    """
    if currency_code not in CURRENCIES:
        return "%s %s" % (currency_code, amount_str)

    currency = CURRENCIES[currency_code]

    # Parse amount
    if '.' in amount_str:
        main_amount, sub_amount = amount_str.split('.')
        main_amount = int(main_amount)
        sub_amount = int(sub_amount)
    else:
        main_amount = int(amount_str)
        sub_amount = 0

    result = "%s %s" % (currency['name'], number_to_words(main_amount))

    if sub_amount > 0:
        result += " " + _na(
            "%s %s" % (currency['subunit'], number_to_words(sub_amount))
        )

    return result
