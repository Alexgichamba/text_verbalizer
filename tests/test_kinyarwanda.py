# tests/test_kinyarwanda.py

"""
Test suite for Kinyarwanda text verbalizer.
"""

import pytest

from verbalizer import KinyarwandaVerbalizer
from verbalizer.languages.kinyarwanda.number import number_to_words


@pytest.fixture
def verbalizer():
    """Fixture to create a KinyarwandaVerbalizer instance."""
    return KinyarwandaVerbalizer()


# ---------------------------------------------------------------------------
# Reference table for Kinyarwanda cardinals.
#
# Two rules govern the output:
#
# 1. CONCORD. A multiplier agrees with the noun class of the scale word it
#    modifies, so the same stem surfaces differently at each scale:
#       3   gatatu   (counting series)
#       30  mirongo *i*tatu    (cl. 4)
#       300 magana  *a*tatu    (cl. 6)
#       3000 ibihumbi *bi*tatu (cl. 8)
#       3 000 000 miliyoni *e*shatu (cl. 9/10)
#
# 2. "NA" AT EVERY JUNCTURE, with vowel elision to "n'". Kinyarwanda differs
#    from Swahili here: Swahili puts "na" before the final component only.
#
# Rows marked NEEDS-REVIEW are the forms I am least sure of and should be
# confirmed by a native speaker before this module is relied on:
#   - 8 and 9 resist the class prefixes (written here as "inani" / "cyenda"
#     across cl. 4/6/8, rather than *binani / *bicyenda)
#   - the class 9/10 series used for miliyoni/miliyari and for "saa"
#   - "makumyabiri" (20) as suppletive, vs. a regular "mirongo ibiri"
#
# Add a row here rather than a bespoke test when covering a new number.
# ---------------------------------------------------------------------------
NUMBER_TABLE = [
    # --- counting / citation series (bare numbers) --------------------------
    (0, "zeru"),
    (1, "rimwe"),
    (2, "kabiri"),
    (3, "gatatu"),
    (4, "kane"),
    (5, "gatanu"),
    (6, "gatandatu"),
    (7, "karindwi"),
    (8, "umunani"),
    (9, "icyenda"),
    (10, "icumi"),
    # --- teens: "icumi" loses its prefix before a unit ----------------------
    (11, "cumi na rimwe"),
    (13, "cumi na gatatu"),
    (15, "cumi na gatanu"),
    (18, "cumi n'umunani"),      # elision before a vowel
    (19, "cumi n'icyenda"),      # elision before a vowel
    # --- tens: 20 is suppletive, 30-90 take cl. 4 concord -------------------
    (20, "makumyabiri"),         # NEEDS-REVIEW (vs. "mirongo ibiri")
    (30, "mirongo itatu"),
    (40, "mirongo ine"),
    (50, "mirongo itanu"),
    (60, "mirongo itandatu"),
    (70, "mirongo irindwi"),
    (80, "mirongo inani"),       # NEEDS-REVIEW
    (90, "mirongo cyenda"),      # NEEDS-REVIEW
    # --- tens + units -------------------------------------------------------
    (21, "makumyabiri na rimwe"),
    (35, "mirongo itatu na gatanu"),
    (45, "mirongo ine na gatanu"),
    (99, "mirongo cyenda n'icyenda"),
    # --- hundreds: 100 is a bare noun, 200-900 take cl. 6 concord -----------
    (100, "ijana"),
    (200, "magana abiri"),
    (300, "magana atatu"),
    (400, "magana ane"),
    (500, "magana atanu"),
    (800, "magana inani"),       # NEEDS-REVIEW
    (900, "magana cyenda"),      # NEEDS-REVIEW
    # --- hundreds + trailing groups, "na" at every juncture ----------------
    (101, "ijana na rimwe"),
    (110, "ijana n'icumi"),
    (150, "ijana na mirongo itanu"),
    (345, "magana atatu na mirongo ine na gatanu"),
    (999, "magana cyenda na mirongo cyenda n'icyenda"),
    # --- thousands: 1000 is a bare noun, 2000+ take cl. 8 concord ----------
    (1000, "igihumbi"),
    (2000, "ibihumbi bibiri"),
    (3000, "ibihumbi bitatu"),
    (5000, "ibihumbi bitanu"),
    (1500, "igihumbi na magana atanu"),
    (2024, "ibihumbi bibiri na makumyabiri na kane"),
    (2345, "ibihumbi bibiri na magana atatu na mirongo ine na gatanu"),
    # a multiplier of ten or more is spelled as a number in its own right
    (10000, "ibihumbi icumi"),
    (15000, "ibihumbi cumi na gatanu"),
    (100000, "ibihumbi ijana"),
    (150000, "ibihumbi ijana na mirongo itanu"),
    # --- millions and billions: cl. 9/10 concord ---------------------------
    (1000000, "miliyoni imwe"),          # NEEDS-REVIEW
    (2000000, "miliyoni ebyiri"),        # NEEDS-REVIEW
    (3000000, "miliyoni eshatu"),        # NEEDS-REVIEW
    (2500000, "miliyoni ebyiri n'ibihumbi magana atanu"),
    (1000000000, "miliyari imwe"),       # NEEDS-REVIEW
]


@pytest.mark.parametrize("value,expected", NUMBER_TABLE)
def test_number_table(value, expected):
    """Every cardinal in the reference table spells out exactly."""
    assert number_to_words(value) == expected


@pytest.mark.parametrize("value,expected", NUMBER_TABLE)
def test_number_table_via_normalize(verbalizer, value, expected):
    """The table also holds end-to-end through ``normalize()``."""
    assert verbalizer.normalize(str(value)) == expected


class TestKinyarwandaConcord:
    """The same stem must surface with the right prefix at each scale."""

    @pytest.mark.parametrize(
        "unit,tens,hundreds,thousands",
        [
            (3, "mirongo itatu", "magana atatu", "ibihumbi bitatu"),
            (4, "mirongo ine", "magana ane", "ibihumbi bine"),
            (5, "mirongo itanu", "magana atanu", "ibihumbi bitanu"),
            (6, "mirongo itandatu", "magana atandatu", "ibihumbi bitandatu"),
            (7, "mirongo irindwi", "magana arindwi", "ibihumbi birindwi"),
        ],
    )
    def test_prefix_differs_per_scale(self, unit, tens, hundreds, thousands):
        """A stem takes cl. 4 / cl. 6 / cl. 8 agreement at 10s / 100s / 1000s."""
        assert number_to_words(unit * 10) == tens
        assert number_to_words(unit * 100) == hundreds
        assert number_to_words(unit * 1000) == thousands

    def test_unit_uses_counting_series(self):
        """A bare unit uses the citation form, not a concord form."""
        assert number_to_words(3) == "gatatu"
        assert number_to_words(3) != "itatu"

    def test_one_is_absorbed_into_the_scale_noun(self):
        """100 and 1000 are bare nouns; they take no "one" multiplier."""
        assert number_to_words(100) == "ijana"
        assert number_to_words(1000) == "igihumbi"


class TestKinyarwandaElision:
    """``na`` elides to ``n'`` before a vowel-initial word."""

    @pytest.mark.parametrize("value", [18, 19, 99, 110])
    def test_elides_before_vowel(self, value):
        assert "n'" in number_to_words(value)
        assert "na i" not in number_to_words(value)
        assert "na u" not in number_to_words(value)

    @pytest.mark.parametrize("value", [21, 35, 150, 345])
    def test_no_elision_before_consonant(self, value):
        assert "na " in number_to_words(value)
        assert "n'" not in number_to_words(value)

    @pytest.mark.parametrize("value,expected", NUMBER_TABLE)
    def test_na_is_never_doubled(self, value, expected):
        """``na`` never appears twice in a row, and never leads or trails."""
        words = number_to_words(value).split()
        assert "na" not in (words[0], words[-1]) or len(words) == 1
        assert not any(a == "na" and b == "na" for a, b in zip(words, words[1:]))


class TestKinyarwandaDecimals:
    """Decimal digits are read one by one after ``akadomo``."""

    def test_simple_decimal(self, verbalizer):
        assert verbalizer.normalize("3.14") == "gatatu akadomo rimwe kane"

    def test_trailing_zero_is_read(self, verbalizer):
        assert verbalizer.normalize("10.5") == "icumi akadomo gatanu"

    def test_leading_zero(self, verbalizer):
        assert verbalizer.normalize("0.99") == "zeru akadomo icyenda icyenda"


class TestKinyarwandaCurrency:
    """Currency verbalization."""

    def test_rwandan_franc(self, verbalizer):
        result = verbalizer.normalize("RWF 10000")
        assert "amafaranga" in result
        assert "ibihumbi icumi" in result

    def test_frw_alias(self, verbalizer):
        assert verbalizer.normalize("FRW 10000") == verbalizer.normalize("RWF 10000")

    def test_dollars(self, verbalizer):
        result = verbalizer.normalize("USD 25")
        assert "amadolari" in result
        assert "makumyabiri na gatanu" in result

    def test_currency_with_subunit(self, verbalizer):
        result = verbalizer.normalize("USD 1500.50")
        assert "santimu" in result
        assert "mirongo itanu" in result

    def test_currency_case_insensitive(self, verbalizer):
        assert verbalizer.normalize("rwf 100") == verbalizer.normalize("RWF 100")

    def test_currency_in_context(self, verbalizer):
        result = verbalizer.normalize("Igiciro ni RWF 5000 gusa")
        assert "amafaranga" in result
        assert "ibihumbi bitanu" in result


class TestKinyarwandaTime:
    """Time verbalization."""

    def test_24h_hours_only(self, verbalizer):
        assert verbalizer.normalize("14:00") == "saa cumi na kane"

    def test_24h_hours_and_minutes(self, verbalizer):
        result = verbalizer.normalize("14:30")
        assert "saa cumi na kane" in result
        assert "iminota mirongo itatu" in result

    def test_hour_uses_class_9_concord(self, verbalizer):
        """Below ten the hour takes the N- series that ``saa`` governs."""
        assert verbalizer.normalize("3:00") == "saa eshatu"
        assert verbalizer.normalize("9:00") == "saa icyenda"

    def test_24h_with_seconds(self, verbalizer):
        result = verbalizer.normalize("14:30:45")
        assert "amasegonda mirongo ine na gatanu" in result

    def test_12h_am(self, verbalizer):
        result = verbalizer.normalize("9:30 AM")
        assert result.endswith("mu gitondo")

    def test_12h_pm(self, verbalizer):
        result = verbalizer.normalize("3:45 PM")
        assert "saa cumi na gatanu" in result  # 3 PM = 15:00
        assert result.endswith("nimugoroba")

    def test_no_meridiem_preserves_following_space(self, verbalizer):
        """A time with no AM/PM must not swallow the space after it."""
        result = verbalizer.normalize("saa 14:30 tariki")
        assert result.endswith("tariki")
        assert "itatutariki" not in result

    def test_digit_run_is_not_a_time(self, verbalizer):
        assert "iminota" not in verbalizer.normalize("igiciro 14:305 gusa")


class TestKinyarwandaDate:
    """Date verbalization."""

    def test_basic_date(self, verbalizer):
        result = verbalizer.normalize("25/12/2024")
        assert result.startswith("tariki ya makumyabiri na gatanu")
        assert "Ukuboza" in result

    def test_all_months(self, verbalizer):
        months = [
            (1, "Mutarama"), (2, "Gashyantare"), (3, "Werurwe"), (4, "Mata"),
            (5, "Gicurasi"), (6, "Kamena"), (7, "Nyakanga"), (8, "Kanama"),
            (9, "Nzeri"), (10, "Ukwakira"), (11, "Ugushyingo"), (12, "Ukuboza"),
        ]
        for month_num, month_name in months:
            assert month_name in verbalizer.normalize("15/%02d/2024" % month_num)

    def test_year_elides_after_wa(self, verbalizer):
        """``wa`` elides before a vowel-initial year, like ``na`` does."""
        result = verbalizer.normalize("15/08/2024")
        assert "mu mwaka w'ibihumbi bibiri" in result
        assert "mwaka wa ibihumbi" not in result

    def test_date_in_context(self, verbalizer):
        result = verbalizer.normalize("Tuzahura ku itariki 15/08/2024")
        assert "Kanama" in result
        assert result.startswith("Tuzahura")


class TestKinyarwandaFullNormalization:
    """Complete text normalization with multiple elements."""

    def test_mixed_content(self, verbalizer):
        text = "Mfite RWF 5000 kandi tuzahura saa 14:30 tariki 25/12/2024"
        result = verbalizer.normalize(text)
        assert "amafaranga" in result
        assert "ibihumbi bitanu" in result
        assert "saa cumi na kane" in result
        assert "Ukuboza" in result

    def test_text_without_normalization_needed(self, verbalizer):
        text = "Muraho neza"
        assert verbalizer.normalize(text) == text

    def test_empty_string(self, verbalizer):
        assert verbalizer.normalize("") == ""

    def test_number_in_context(self, verbalizer):
        assert verbalizer.normalize("Mfite abana 3") == "Mfite abana gatatu"


class TestKinyarwandaIndividualNormalizers:
    """Each normalizer touches only its own semiotic class."""

    def test_normalize_numbers_only(self, verbalizer):
        result = verbalizer.normalize_numbers("Mfite 3 abana na RWF 100")
        assert "gatatu" in result
        assert "RWF" in result

    def test_normalize_currency_only(self, verbalizer):
        result = verbalizer.normalize_currency("Igiciro ni RWF 100 ku bana 3")
        assert "amafaranga" in result
        assert "3" in result

    def test_normalize_time_only(self, verbalizer):
        result = verbalizer.normalize_time("Saa 14:30 igiciro ni 100")
        assert "saa cumi na kane" in result
        assert "100" in result

    def test_normalize_dates_only(self, verbalizer):
        result = verbalizer.normalize_dates("Tariki 25/12/2024 igiciro ni 100")
        assert "Ukuboza" in result
        assert "100" in result


class TestKinyarwandaDigitMode:
    """Reading a bare run of digits one digit at a time."""

    def test_leading_zero_is_read_as_digits_by_default(self):
        """A leading zero marks an identifier, so "auto" reads it out."""
        v = KinyarwandaVerbalizer()
        assert v.normalize("0793092164") == "zeru karindwi icyenda gatatu zeru icyenda kabiri rimwe gatandatu kane"

    def test_leading_zero_survives(self):
        """The zero itself must not be lost, as int() would lose it."""
        v = KinyarwandaVerbalizer()
        assert v.normalize("0793092164").startswith("zeru")

    def test_ordinary_number_still_reads_as_a_cardinal(self):
        """"auto" must not disturb a plain quantity."""
        v = KinyarwandaVerbalizer()
        assert v.normalize("2345") == number_to_words(2345)

    def test_never_forces_the_cardinal_reading(self):
        v = KinyarwandaVerbalizer(read_digits="never")
        assert v.normalize("0793092164") == number_to_words(793092164)

    def test_always_forces_the_digit_reading(self):
        v = KinyarwandaVerbalizer(read_digits="always")
        assert v.normalize("2345") == "kabiri gatatu kane gatanu"

    def test_digit_threshold_catches_a_number_without_a_leading_zero(self):
        """A phone number written without its leading zero needs a threshold."""
        plain = KinyarwandaVerbalizer()
        assert plain.normalize("250793092164") == number_to_words(250793092164)

        thresholded = KinyarwandaVerbalizer(digit_threshold=7)
        assert thresholded.normalize("250793092164") == "kabiri gatanu zeru karindwi icyenda gatatu zeru icyenda kabiri rimwe gatandatu kane"

    def test_threshold_leaves_short_numbers_alone(self):
        v = KinyarwandaVerbalizer(digit_threshold=7)
        assert v.normalize("345") == number_to_words(345)

    def test_digits_are_juxtaposed_without_na(self):
        """A digit sequence is a list, not a sum, so it takes no "na"."""
        v = KinyarwandaVerbalizer(read_digits="always")
        assert " na " not in v.normalize("0793092164")
        assert "n'" not in v.normalize("0793092164")

    def test_invalid_mode_is_rejected(self):
        with pytest.raises(ValueError):
            KinyarwandaVerbalizer(read_digits="sometimes")

    def test_currency_is_unaffected(self):
        """Digit mode applies to bare numbers, not to currency amounts."""
        v = KinyarwandaVerbalizer(read_digits="always")
        assert "ijana" in v.normalize("RWF 100")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
