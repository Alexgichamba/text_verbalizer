# tests/test_swahili.py

"""
Test suite for Swahili text verbalizer.
"""

import pytest
from verbalizer import SwahiliVerbalizer
from verbalizer.languages.swahili.number import number_to_words


@pytest.fixture
def verbalizer():
    """Fixture to create a SwahiliVerbalizer instance."""
    return SwahiliVerbalizer()


class TestSwahiliNumbers:
    """Test number verbalization."""
    
    def test_single_digits(self, verbalizer):
        """Test single digit numbers."""
        assert verbalizer.normalize("0") == "sifuri"
        assert verbalizer.normalize("1") == "moja"
        assert verbalizer.normalize("5") == "tano"
        assert verbalizer.normalize("9") == "tisa"
    
    def test_teens(self, verbalizer):
        """Test numbers 10-19."""
        assert verbalizer.normalize("10") == "kumi"
        assert verbalizer.normalize("15") == "kumi na tano"
        assert verbalizer.normalize("19") == "kumi na tisa"
    
    def test_tens(self, verbalizer):
        """Test tens (20, 30, 40, etc.)."""
        assert verbalizer.normalize("20") == "ishirini"
        assert verbalizer.normalize("30") == "thelathini"
        assert verbalizer.normalize("50") == "hamsini"
        assert verbalizer.normalize("90") == "tisini"
    
    def test_compound_tens(self, verbalizer):
        """Test compound numbers in tens range."""
        assert verbalizer.normalize("21") == "ishirini na moja"
        assert verbalizer.normalize("45") == "arobaini na tano"
        assert verbalizer.normalize("99") == "tisini na tisa"
    
    def test_hundreds(self, verbalizer):
        """Test hundreds."""
        assert verbalizer.normalize("100") == "mia moja"
        assert verbalizer.normalize("200") == "mia mbili"
        assert verbalizer.normalize("500") == "mia tano"
        assert verbalizer.normalize("900") == "mia tisa"
    
    def test_compound_hundreds(self, verbalizer):
        """Test compound numbers with hundreds."""
        assert verbalizer.normalize("150") == "mia moja na hamsini"
        assert verbalizer.normalize("325") == "mia tatu ishirini na tano"
        assert verbalizer.normalize("999") == "mia tisa tisini na tisa"
    
    def test_thousands(self, verbalizer):
        """Test thousands."""
        assert verbalizer.normalize("1000") == "elfu moja"
        assert verbalizer.normalize("2000") == "elfu mbili"
        assert verbalizer.normalize("10000") == "elfu kumi"
        assert verbalizer.normalize("50000") == "elfu hamsini"
    
    def test_compound_thousands(self, verbalizer):
        """Test compound numbers with thousands."""
        assert verbalizer.normalize("1500") == "elfu moja na mia tano"
        assert verbalizer.normalize("2024") == "elfu mbili ishirini na nne"
        assert verbalizer.normalize("15250") == "elfu kumi na tano mia mbili na hamsini"
    
    def test_millions(self, verbalizer):
        """Test millions."""
        assert verbalizer.normalize("1000000") == "milioni moja"
        assert verbalizer.normalize("5000000") == "milioni tano"
        assert verbalizer.normalize("10000000") == "milioni kumi"
    
    def test_billions(self, verbalizer):
        """Test billions."""
        assert verbalizer.normalize("1000000000") == "bilioni moja"
        assert verbalizer.normalize("2000000000") == "bilioni mbili"
    
    def test_decimal_numbers(self, verbalizer):
        """Test decimal numbers."""
        assert verbalizer.normalize("3.14") == "tatu nukta moja nne"
        assert verbalizer.normalize("10.5") == "kumi nukta tano"
        assert verbalizer.normalize("0.99") == "sifuri nukta tisa tisa"
    
    def test_negative_numbers(self, verbalizer):
        """Test negative numbers."""
        assert verbalizer.normalize("-5") == "hasi tano"
        assert verbalizer.normalize("-100") == "hasi mia moja"
    
    def test_numbers_in_context(self, verbalizer):
        """Test numbers within sentences."""
        assert "tatu" in verbalizer.normalize("Nina watoto 3")
        assert "kumi" in verbalizer.normalize("Bei ni 10 shilingi")


# ---------------------------------------------------------------------------
# Reference table for Swahili cardinals.
#
# The governing rule is that ``na`` is placed before the FINAL additive
# component only; earlier components are juxtaposed. A number decomposes into
# scale groups ("elfu mbili", "mia tatu") plus a trailing tens/ones group, and
# only the last of those takes ``na``. A scale multiplier is a number in its
# own right and carries its own internal ``na`` (15000 -> "elfu kumi na tano").
#
# Add a row here rather than a bespoke test when covering a new number.
# ---------------------------------------------------------------------------
NUMBER_TABLE = [
    # --- units -------------------------------------------------------------
    (0, "sifuri"),
    (1, "moja"),
    (2, "mbili"),
    (3, "tatu"),
    (4, "nne"),
    (5, "tano"),
    (6, "sita"),
    (7, "saba"),
    (8, "nane"),
    (9, "tisa"),
    # --- 10-19: single "na", nothing before it -----------------------------
    (10, "kumi"),
    (11, "kumi na moja"),
    (15, "kumi na tano"),
    (19, "kumi na tisa"),
    # --- round tens --------------------------------------------------------
    (20, "ishirini"),
    (30, "thelathini"),
    (40, "arobaini"),
    (50, "hamsini"),
    (60, "sitini"),
    (70, "sabini"),
    (80, "themanini"),
    (90, "tisini"),
    # --- tens + units ------------------------------------------------------
    (21, "ishirini na moja"),
    (45, "arobaini na tano"),
    (99, "tisini na tisa"),
    # --- hundreds: multiplier FOLLOWS the scale word, and 100 keeps "moja" --
    (100, "mia moja"),
    (200, "mia mbili"),
    (900, "mia tisa"),
    # --- hundreds + one trailing group: that group takes "na" --------------
    (101, "mia moja na moja"),
    (110, "mia moja na kumi"),
    (150, "mia moja na hamsini"),
    # --- hundreds + two trailing groups: only the LAST takes "na" ----------
    # This is the case the old implementation over-generated on, emitting
    # "mia tatu na ishirini na tano".
    (325, "mia tatu ishirini na tano"),
    (345, "mia tatu arobaini na tano"),
    (999, "mia tisa tisini na tisa"),
    # --- thousands ---------------------------------------------------------
    (1000, "elfu moja"),
    (2000, "elfu mbili"),
    (10000, "elfu kumi"),
    (50000, "elfu hamsini"),
    (1500, "elfu moja na mia tano"),
    (2024, "elfu mbili ishirini na nne"),
    (2345, "elfu mbili mia tatu arobaini na tano"),
    # multiplier carries its own "na", trailing group carries the outer one
    (15000, "elfu kumi na tano"),
    (15250, "elfu kumi na tano mia mbili na hamsini"),
    (150000, "elfu mia moja na hamsini"),
    # --- millions and billions --------------------------------------------
    (1000000, "milioni moja"),
    (5000000, "milioni tano"),
    (10000000, "milioni kumi"),
    (2500000, "milioni mbili na elfu mia tano"),
    (1000000000, "bilioni moja"),
    (2000000000, "bilioni mbili"),
]


@pytest.mark.parametrize("value,expected", NUMBER_TABLE)
def test_number_table(value, expected):
    """Every cardinal in the reference table spells out exactly."""
    assert number_to_words(value) == expected


@pytest.mark.parametrize("value,expected", NUMBER_TABLE)
def test_number_table_via_normalize(verbalizer, value, expected):
    """The table also holds end-to-end through ``normalize()``."""
    assert verbalizer.normalize(str(value)) == expected


@pytest.mark.parametrize("value,expected", NUMBER_TABLE)
def test_na_is_never_doubled(value, expected):
    """``na`` never appears twice in a row, and never leads or trails."""
    words = number_to_words(value).split()
    assert "na" not in (words[0], words[-1]) or len(words) == 1
    assert not any(a == "na" and b == "na" for a, b in zip(words, words[1:]))


class TestSwahiliCurrency:
    """Test currency verbalization."""
    
    def test_kenyan_shilling(self, verbalizer):
        """Test Kenyan Shilling (KES)."""
        result = verbalizer.normalize("KES 100")
        assert "shilingi" in result
        assert "mia moja" in result
        
        result = verbalizer.normalize("KES 1500")
        assert "shilingi" in result
        assert "elfu moja" in result
    
    def test_tanzanian_shilling(self, verbalizer):
        """Test Tanzanian Shilling (TZS)."""
        result = verbalizer.normalize("TZS 5000")
        assert "shilingi" in result
        assert "elfu tano" in result
    
    def test_nigerian_naira(self, verbalizer):
        """Test Nigerian Naira (NGN)."""
        result = verbalizer.normalize("NGN 2500")
        assert "naira" in result
        assert "elfu mbili" in result
    
    def test_rwandan_franc(self, verbalizer):
        """Test Rwandan Franc (RWF)."""
        result = verbalizer.normalize("RWF 10000")
        assert "faranga" in result
        assert "elfu kumi" in result
    
    def test_currency_with_decimals(self, verbalizer):
        """Test currency with decimal subunits."""
        result = verbalizer.normalize("KES 150.50")
        assert "shilingi" in result
        assert "senti" in result
        assert "hamsini" in result
    
    def test_currency_case_insensitive(self, verbalizer):
        """Test that currency codes are case-insensitive."""
        result1 = verbalizer.normalize("kes 100")
        result2 = verbalizer.normalize("KES 100")
        assert result1 == result2
    
    def test_currency_in_context(self, verbalizer):
        """Test currency within sentences."""
        result = verbalizer.normalize("Bei ni KES 5000 tu")
        assert "shilingi" in result
        assert "elfu tano" in result


class TestSwahiliTime:
    """Test time verbalization."""
    
    def test_24h_hours_only(self, verbalizer):
        """Test 24-hour format with hours only (no minutes)."""
        result = verbalizer.normalize("14:00")
        assert "saa kumi na nne" in result
    
    def test_24h_hours_and_minutes(self, verbalizer):
        """Test 24-hour format with hours and minutes."""
        result = verbalizer.normalize("14:30")
        assert "saa kumi na nne" in result
        assert "dakika thelathini" in result
    
    def test_24h_with_seconds(self, verbalizer):
        """Test 24-hour format with seconds."""
        result = verbalizer.normalize("14:30:45")
        assert "saa kumi na nne" in result
        assert "dakika thelathini" in result
        assert "sekunde arobaini na tano" in result
    
    def test_12h_am_format(self, verbalizer):
        """Test 12-hour AM format."""
        result = verbalizer.normalize("9:30 AM")
        assert "saa tisa" in result
        assert "dakika thelathini" in result
        assert "asubuhi" in result
    
    def test_12h_pm_format(self, verbalizer):
        """Test 12-hour PM format."""
        result = verbalizer.normalize("3:45 PM")
        assert "saa kumi na tano" in result  # 3 PM = 15:00 in 24h
        assert "dakika arobaini na tano" in result
        assert "jioni" in result
    
    def test_midnight(self, verbalizer):
        """Test midnight (12:00 AM)."""
        result = verbalizer.normalize("12:00 AM")
        assert "saa sifuri" in result
        assert "asubuhi" in result
    
    def test_noon(self, verbalizer):
        """Test noon (12:00 PM)."""
        result = verbalizer.normalize("12:00 PM")
        assert "saa kumi na mbili" in result
        assert "jioni" in result
    
    def test_no_meridiem_preserves_following_space(self, verbalizer):
        """A time with no AM/PM must not swallow the space after it.

        The pattern used to end in ``\\s*(AM|PM)?\\b``, so the optional
        meridiem matched empty *after* ``\\s*`` had already consumed the
        separator, gluing the next word onto the output.
        """
        result = verbalizer.normalize("saa 14:30 tarehe")
        assert result == "saa saa kumi na nne na dakika thelathini tarehe"
        assert "thelathinitarehe" not in result

    def test_no_meridiem_preserves_space_with_seconds(self, verbalizer):
        """Same, for the hh:mm:ss form."""
        result = verbalizer.normalize("14:30:45 sasa")
        assert result.endswith("sekunde arobaini na tano sasa")

    def test_meridiem_still_consumes_its_space(self, verbalizer):
        """The space before an actual AM/PM is still part of the match."""
        assert verbalizer.normalize("3:45 PM leo").startswith("saa kumi na tano")
        assert verbalizer.normalize("3:45 PM leo").endswith("jioni leo")

    def test_meridiem_without_space(self, verbalizer):
        """AM/PM directly attached to the time still parses."""
        result = verbalizer.normalize("2:30pm leo")
        assert "saa kumi na nne" in result
        assert result.endswith("jioni leo")

    def test_digit_run_is_not_a_time(self, verbalizer):
        """``14:305`` is not a time; the (?!\\d) guard rejects it."""
        assert "saa kumi na nne na dakika thelathini" not in verbalizer.normalize(
            "bei 14:305 tu"
        )

    def test_time_in_context(self, verbalizer):
        """Test time within sentences."""
        result = verbalizer.normalize("Tutaonana saa 14:30")
        assert "saa kumi na nne" in result
        assert "dakika thelathini" in result


class TestSwahiliDate:
    """Test date verbalization."""
    
    def test_basic_date(self, verbalizer):
        """Test basic date format."""
        result = verbalizer.normalize("25/12/2024")
        assert "tarehe" in result
        assert "ishirini na tano" in result
        assert "Desemba" in result
        assert "elfu mbili" in result
    
    def test_all_months(self, verbalizer):
        """Test all months are recognized."""
        months = [
            (1, "Januari"),
            (2, "Februari"),
            (3, "Machi"),
            (4, "Aprili"),
            (5, "Mei"),
            (6, "Juni"),
            (7, "Julai"),
            (8, "Agosti"),
            (9, "Septemba"),
            (10, "Oktoba"),
            (11, "Novemba"),
            (12, "Desemba"),
        ]
        
        for month_num, month_name in months:
            result = verbalizer.normalize(f"15/{month_num:02d}/2024")
            assert month_name in result
    
    def test_first_day_of_month(self, verbalizer):
        """Test first day of month."""
        result = verbalizer.normalize("01/01/2024")
        assert "moja" in result
        assert "Januari" in result
    
    def test_last_day_of_month(self, verbalizer):
        """Test last day of month."""
        result = verbalizer.normalize("31/12/2024")
        assert "thelathini na moja" in result
        assert "Desemba" in result
    
    def test_date_in_context(self, verbalizer):
        """Test date within sentences."""
        result = verbalizer.normalize("Tutaonana tarehe 15/08/2024")
        assert "tarehe" in result
        assert "kumi na tano" in result
        assert "Agosti" in result


class TestSwahiliFullNormalization:
    """Test complete text normalization with multiple elements."""
    
    def test_mixed_content(self, verbalizer):
        """Test text with numbers, currency, time, and dates."""
        text = "Nina KES 5000 na tutaonana saa 14:30 tarehe 25/12/2024"
        result = verbalizer.normalize(text)
        
        # Check that all components are normalized
        assert "shilingi" in result
        assert "elfu tano" in result
        assert "saa kumi na nne" in result
        assert "dakika thelathini" in result
        assert "tarehe" in result
        assert "Desemba" in result
    
    def test_multiple_numbers(self, verbalizer):
        """Test text with multiple numbers."""
        text = "Nina watoto 3 na gari 1"
        result = verbalizer.normalize(text)
        assert "tatu" in result
        assert "moja" in result
    
    def test_multiple_currencies(self, verbalizer):
        """Test text with multiple currency amounts."""
        text = "Bei ni KES 1000 au TZS 5000"
        result = verbalizer.normalize(text)
        assert result.count("shilingi") == 2
        assert "elfu moja" in result
        assert "elfu tano" in result
    
    def test_text_without_normalization_needed(self, verbalizer):
        """Test that regular text passes through unchanged."""
        text = "Habari yako leo"
        result = verbalizer.normalize(text)
        assert result == text
    
    def test_empty_string(self, verbalizer):
        """Test empty string handling."""
        result = verbalizer.normalize("")
        assert result == ""
    
    def test_whitespace_preservation(self, verbalizer):
        """Test that whitespace is generally preserved."""
        text = "Nina   watoto 3"
        result = verbalizer.normalize(text)
        # Should have normalized the number but kept spacing
        assert "tatu" in result


class TestSwahiliIndividualNormalizers:
    """Test individual normalization methods."""
    
    def test_normalize_numbers_only(self, verbalizer):
        """Test that normalize_numbers only normalizes numbers."""
        text = "Nina 3 watoto na KES 100"
        result = verbalizer.normalize_numbers(text)
        assert "tatu" in result
        assert "KES" in result  # Currency not normalized
    
    def test_normalize_currency_only(self, verbalizer):
        """Test that normalize_currency only normalizes currency."""
        text = "Bei ni KES 100 kwa watoto 3"
        result = verbalizer.normalize_currency(text)
        assert "shilingi" in result
        assert "3" in result  # Number not normalized
    
    def test_normalize_time_only(self, verbalizer):
        """Test that normalize_time only normalizes time."""
        text = "Saa 14:30 na bei ni 100"
        result = verbalizer.normalize_time(text)
        assert "saa kumi na nne" in result
        assert "100" in result  # Number not normalized
    
    def test_normalize_dates_only(self, verbalizer):
        """Test that normalize_dates only normalizes dates."""
        text = "Tarehe 25/12/2024 na bei ni 100"
        result = verbalizer.normalize_dates(text)
        assert "tarehe" in result
        assert "Desemba" in result
        assert "100" in result  # Number not normalized


class TestSwahiliDigitMode:
    """Reading a bare run of digits one digit at a time."""

    def test_leading_zero_is_read_as_digits_by_default(self):
        """A leading zero marks an identifier, so "auto" reads it out."""
        v = SwahiliVerbalizer()
        assert v.normalize("0712345678") == "sifuri saba moja mbili tatu nne tano sita saba nane"

    def test_leading_zero_survives(self):
        """The zero itself must not be lost, as int() would lose it."""
        v = SwahiliVerbalizer()
        assert v.normalize("0712345678").startswith("sifuri")

    def test_ordinary_number_still_reads_as_a_cardinal(self):
        """"auto" must not disturb a plain quantity."""
        v = SwahiliVerbalizer()
        assert v.normalize("2345") == number_to_words(2345)

    def test_never_forces_the_cardinal_reading(self):
        v = SwahiliVerbalizer(read_digits="never")
        assert v.normalize("0712345678") == number_to_words(712345678)

    def test_always_forces_the_digit_reading(self):
        v = SwahiliVerbalizer(read_digits="always")
        assert v.normalize("2345") == "mbili tatu nne tano"

    def test_digit_threshold_catches_a_number_without_a_leading_zero(self):
        """A phone number written without its leading zero needs a threshold."""
        plain = SwahiliVerbalizer()
        assert plain.normalize("254712345678") == number_to_words(254712345678)

        thresholded = SwahiliVerbalizer(digit_threshold=7)
        assert thresholded.normalize("254712345678") == "mbili tano nne saba moja mbili tatu nne tano sita saba nane"

    def test_threshold_leaves_short_numbers_alone(self):
        v = SwahiliVerbalizer(digit_threshold=7)
        assert v.normalize("345") == number_to_words(345)

    def test_digits_are_juxtaposed_without_na(self):
        """A digit sequence is a list, not a sum, so it takes no "na"."""
        v = SwahiliVerbalizer(read_digits="always")
        assert " na " not in v.normalize("0712345678")
        assert "n'" not in v.normalize("0712345678")

    def test_invalid_mode_is_rejected(self):
        with pytest.raises(ValueError):
            SwahiliVerbalizer(read_digits="sometimes")

    def test_currency_is_unaffected(self):
        """Digit mode applies to bare numbers, not to currency amounts."""
        v = SwahiliVerbalizer(read_digits="always")
        assert "mia moja" in v.normalize("KES 100")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])