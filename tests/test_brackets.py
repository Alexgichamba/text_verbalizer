"""Tests for bracketed inline control spans.

TTS front-ends carry inline markup in square brackets -- OmniVoice uses
``[laughter]`` for non-verbal tags and ``[B EY1 S]`` for CMU pronunciation
overrides. That markup is not speech, so the verbalizer must not read the
digits inside it.
"""

import pytest

from verbalizer import KinyarwandaVerbalizer, SwahiliVerbalizer

VERBALIZERS = [KinyarwandaVerbalizer, SwahiliVerbalizer]


@pytest.mark.parametrize("cls", VERBALIZERS)
class TestBracketProtection:
    def test_non_verbal_tag_survives(self, cls):
        out = cls().normalize("Nagize 12 [laughter] amafaranga.")
        assert "[laughter]" in out
        assert "12" not in out

    def test_digits_inside_a_tag_are_not_read(self, cls):
        """A bracketed count must stay markup, not become a spoken number."""
        assert cls().normalize("[laughter 2]") == "[laughter 2]"

    def test_cmu_stress_digit_survives(self, cls):
        """``[B EY1 S]``'s stress digit would otherwise be read aloud."""
        assert cls().normalize("The [B EY1 S] guitar.") == "The [B EY1 S] guitar."

    def test_text_on_both_sides_is_normalized(self, cls):
        out = cls().normalize("5 [sigh] 5")
        spoken = out.split(" [sigh] ")
        assert len(spoken) == 2
        assert spoken[0] == spoken[1]
        assert "5" not in out

    def test_spacing_around_a_tag_is_preserved(self, cls):
        assert cls().normalize("a [sigh] b") == "a [sigh] b"

    def test_multiple_tags(self, cls):
        out = cls().normalize("[a] 7 [b] 7 [c]")
        assert out.startswith("[a] ") and out.endswith(" [c]")
        assert "7" not in out

    def test_protection_can_be_disabled(self, cls):
        out = cls(protect_brackets=False).normalize("[laughter 2]")
        assert out != "[laughter 2]"

    def test_unmatched_bracket_is_left_alone(self, cls):
        """A stray ``[`` is not a span; the text is still normalized."""
        out = cls().normalize("[ 5")
        assert "5" not in out
