# verbalizer/languages/kinyarwanda/number.py

"""
Kinyarwanda number verbalization.

Unlike Swahili, Kinyarwanda numerals carry **noun-class concord**: the same
numeral stem takes a different prefix depending on the class of the noun it
counts. The scale words are themselves nouns of fixed class, so a multiplier
agrees with its scale word:

    mirongo   (cl. 4)  ->  mirongo *i*tatu    (30)
    magana    (cl. 6)  ->  magana *a*tatu     (300)
    ibihumbi  (cl. 8)  ->  ibihumbi *bi*tatu  (3000)
    miliyoni  (cl. 9)  ->  miliyoni *e*shatu  (3 000 000)

The prefixes are not fully regular (8 and 9 resist them, 20 is suppletive), so
each series is spelled out as an explicit table rather than derived from a
stem plus a prefix.

A bare number in running text has no noun to agree with, so units fall back to
the **counting / citation** series (rimwe, kabiri, gatatu, ...). That is the
right choice for TTS, but it means an attributive reading ("abantu babiri",
"ibitabo bibiri") is out of reach without knowing the counted noun -- see the
module README for the limits of context-free verbalization.
"""

# --- Counting (citation) series -------------------------------------------
# Used for a bare number and for the trailing units group.
COUNTING = {
    0: "zeru",
    1: "rimwe",
    2: "kabiri",
    3: "gatatu",
    4: "kane",
    5: "gatanu",
    6: "gatandatu",
    7: "karindwi",
    8: "umunani",
    9: "icyenda",
    10: "icumi",
}

# --- Concord series, keyed by the class of the scale word they modify ------
# Class 4 (i-): multipliers of "mirongo" (tens).
CONCORD_TENS = {
    2: "ibiri",
    3: "itatu",
    4: "ine",
    5: "itanu",
    6: "itandatu",
    7: "irindwi",
    8: "inani",
    9: "cyenda",
}

# Class 6 (a-): multipliers of "magana" (hundreds).
CONCORD_HUNDREDS = {
    2: "abiri",
    3: "atatu",
    4: "ane",
    5: "atanu",
    6: "atandatu",
    7: "arindwi",
    8: "inani",
    9: "cyenda",
}

# Class 8 (bi-): multipliers of "ibihumbi" (thousands).
CONCORD_THOUSANDS = {
    2: "bibiri",
    3: "bitatu",
    4: "bine",
    5: "bitanu",
    6: "bitandatu",
    7: "birindwi",
    8: "inani",
    9: "cyenda",
}

# Class 9/10 (N-): multipliers of the loanwords "miliyoni" and "miliyari",
# and of "saa" in time expressions.
CONCORD_N = {
    1: "imwe",
    2: "ebyiri",
    3: "eshatu",
    4: "enye",
    5: "eshanu",
    6: "esheshatu",
    7: "indwi",
    8: "inani",
    9: "icyenda",
    10: "icumi",
}

# --- Scale words -----------------------------------------------------------
TEN = "icumi"            # standalone 10
TEN_COMBINING = "cumi"   # 10 when a unit follows: "cumi na gatatu"
TWENTY = "makumyabiri"   # suppletive; not "mirongo ibiri"
TENS = "mirongo"
HUNDRED = "ijana"        # 100 is a bare noun, with no multiplier
HUNDREDS = "magana"
THOUSAND = "igihumbi"    # 1000 is a bare noun, with no multiplier
THOUSANDS = "ibihumbi"
MILLION = "miliyoni"
BILLION = "miliyari"

NEGATIVE = "negatifu"
POINT = "akadomo"

_VOWELS = "aeiou"


def _na(word):
    """Return the conjunction ``na`` with vowel elision before ``word``.

    Kinyarwanda elides the vowel of ``na`` before a vowel-initial word:
    ``na icyenda`` -> ``n'icyenda``, but ``na gatatu`` stays as it is.
    """
    return "n'" + word if word[:1].lower() in _VOWELS else "na " + word


def _join_components(parts):
    """Join additive components, inserting ``na`` before every one but the first.

    Kinyarwanda -- unlike Swahili, which uses ``na`` only before the final
    component -- links every juncture: 2345 is
    "ibihumbi bibiri na magana atatu na mirongo ine na gatanu".
    """
    out = parts[0]
    for part in parts[1:]:
        out += " " + _na(part)
    return out


def _multiplier(n, concord):
    """Spell the multiplier of a scale word using ``concord`` for 1-9.

    Multipliers of ten and above are numbers in their own right and are spelled
    with the general (counting) forms: "ibihumbi cumi na gatanu" (15 000).
    """
    if n < 10 and n in concord:
        return concord[n]
    return _join_components(_components(n))


def _components(n):
    """Decompose a non-negative integer into its additive spoken components."""
    if n == 0:
        return [COUNTING[0]]

    if n >= 1_000_000_000:
        multiplier, remainder = divmod(n, 1_000_000_000)
        parts = ["%s %s" % (BILLION, _multiplier(multiplier, CONCORD_N))]
        if remainder:
            parts.extend(_components(remainder))
        return parts

    if n >= 1_000_000:
        multiplier, remainder = divmod(n, 1_000_000)
        parts = ["%s %s" % (MILLION, _multiplier(multiplier, CONCORD_N))]
        if remainder:
            parts.extend(_components(remainder))
        return parts

    if n >= 1000:
        multiplier, remainder = divmod(n, 1000)
        if multiplier == 1:
            parts = [THOUSAND]
        else:
            parts = ["%s %s" % (THOUSANDS, _multiplier(multiplier, CONCORD_THOUSANDS))]
        if remainder:
            parts.extend(_components(remainder))
        return parts

    if n >= 100:
        multiplier, remainder = divmod(n, 100)
        if multiplier == 1:
            parts = [HUNDRED]
        else:
            parts = ["%s %s" % (HUNDREDS, CONCORD_HUNDREDS[multiplier])]
        if remainder:
            parts.extend(_components(remainder))
        return parts

    if n >= 10:
        tens_digit, ones_digit = divmod(n, 10)
        if tens_digit == 1:
            # 10 alone is "icumi"; with a unit following it loses its prefix.
            parts = [TEN_COMBINING if ones_digit else TEN]
        elif tens_digit == 2:
            parts = [TWENTY]
        else:
            parts = ["%s %s" % (TENS, CONCORD_TENS[tens_digit])]
        if ones_digit:
            parts.append(COUNTING[ones_digit])
        return parts

    return [COUNTING[n]]


def number_to_words(n):
    """
    Convert an integer to Kinyarwanda words.

    Args:
        n (int): Number to convert (0 to 999,999,999,999)

    Returns:
        str: Kinyarwanda word representation
    """
    if n < 0:
        return "%s %s" % (NEGATIVE, number_to_words(-n))

    return _join_components(_components(n))


def verbalize_number(number_str):
    """
    Convert a number string to Kinyarwanda words.
    Handles integers and decimals.

    Args:
        number_str (str): String representation of a number

    Returns:
        str: Verbalized number in Kinyarwanda
    """
    number_str = number_str.strip()

    if '.' in number_str:
        integer_part, decimal_part = number_str.split('.')

        result = number_to_words(int(integer_part))
        result += " " + POINT

        # Read each decimal digit separately.
        for digit in decimal_part:
            result += " %s" % COUNTING[int(digit)]

        return result

    return number_to_words(int(number_str))


def digit_string(number_str):
    """Read a run of digits one at a time, in Kinyarwanda.

    Used for identifiers -- phone numbers, account and ID numbers -- where
    the cardinal reading is wrong and a leading zero is significant:
    "0793092164" is "zeru karindwi icyenda gatatu ...", not a number in the
    hundreds of millions.

    Digits take the counting (citation) series, and are juxtaposed with no
    linking "na" -- a digit sequence is a list, not a sum.
    """
    words = []
    for char in number_str.strip():
        if char.isdigit():
            words.append(COUNTING[int(char)])
        elif char == '.':
            words.append(POINT)
        # any other character (a separator such as - or /) is simply dropped
    return " ".join(words)
