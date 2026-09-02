# Text Verbalizer

A rule-based text verbalizer library for African languages, designed for speech applications.

## Features

- **Number Verbalization**: Convert digits to words
- **Currency Support**: Handle multiple African currencies (KES, TZS, NGN, RWF)
- **Time Normalization**: Convert time expressions to words
- **Date Verbalization**: Convert dates to spoken form
- **Extensible Architecture**: Easy to add new languages

## Currently Supported Languages

- **Swahili** (Kiswahili) - Full support
- **Kinyarwanda** - Full support (numbers, currency, time, dates)

> **Note on Kinyarwanda.** Numerals carry noun-class concord: a multiplier
> agrees with the class of the scale word it modifies, so the same stem
> surfaces as `gatatu` (3), `mirongo itatu` (30), `magana atatu` (300) and
> `ibihumbi bitatu` (3000). A bare number in running text has no noun to agree
> with, so units use the counting/citation series. An attributive reading
> (`abantu babiri`, `ibitabo bibiri`) needs the counted noun and is out of
> reach for a context-free verbalizer. Forms marked `NEEDS-REVIEW` in
> `tests/test_kinyarwanda.py` are the ones awaiting native-speaker
> confirmation.

## Installation

```bash
pip install -e .
```

## Quick Start

```python
from verbalizer import SwahiliVerbalizer

# Initialize verbalizer
verbalizer = SwahiliVerbalizer()

# Normalize text
text = "Nina KES 5000 na saa ni 14:30 tarehe 25/12/2024"
normalized = verbalizer.normalize(text)
print(normalized)
# Output: "Nina shilingi elfu tano na saa ni saa kumi na nne na dakika thelathini tarehe tarehe ishirini na tano mwezi wa Desemba mwaka elfu mbili ishirini na nne"
```

## Usage Examples

### Number Normalization

```python
verbalizer = SwahiliVerbalizer()

# Basic numbers
print(verbalizer.normalize("Nina watoto 3"))
# Output: "Nina watoto tatu"

# Large numbers
print(verbalizer.normalize("Bei ni 150000"))
# Output: "Bei ni elfu mia moja na hamsini"
```

### Currency Normalization

```python
# Kenyan Shilling
print(verbalizer.normalize("KES 1500.50"))
# Output: "shilingi elfu moja na mia tano na senti hamsini"

# Tanzanian Shilling
print(verbalizer.normalize("TZS 50000"))
# Output: "shilingi elfu hamsini"

# Nigerian Naira
print(verbalizer.normalize("NGN 2500"))
# Output: "naira elfu mbili na mia tano"

# Rwandan Franc
print(verbalizer.normalize("RWF 10000"))
# Output: "faranga elfu kumi"
```

### Time Normalization

```python
# 24-hour format
print(verbalizer.normalize("Saa ni 14:30"))
# Output: "Saa ni saa kumi na nne na dakika thelathini"

# 12-hour format
print(verbalizer.normalize("Tutaonana 3:45 PM"))
# Output: "Tutaonana saa kumi na tano na dakika arobaini na tano jioni"
```

### Date Normalization

```python
print(verbalizer.normalize("Tarehe 15/08/2024"))
# Output: "Tarehe tarehe kumi na tano mwezi wa Agosti mwaka elfu mbili na ishirini na nne"
```

### Kinyarwanda

```python
from verbalizer import KinyarwandaVerbalizer

verbalizer = KinyarwandaVerbalizer()

print(verbalizer.normalize("Mfite amafaranga 2345"))
# Output: "Mfite amafaranga ibihumbi bibiri na magana atatu na mirongo ine na gatanu"

print(verbalizer.normalize("RWF 10000"))
# Output: "amafaranga y'u Rwanda ibihumbi icumi"

print(verbalizer.normalize("Tuzahura saa 14:30"))
# Output: "Tuzahura saa saa cumi na kane n'iminota mirongo itatu"

print(verbalizer.normalize("15/08/2024"))
# Output: "tariki ya cumi na gatanu Kanama mu mwaka w'ibihumbi bibiri na makumyabiri na kane"
```

### Reading digits one at a time

Phone numbers, account numbers and IDs must not be read as quantities, and
their leading zero is significant. `read_digits` controls this:

```python
verbalizer = KinyarwandaVerbalizer()          # read_digits="auto" (default)

print(verbalizer.normalize("Nimero yanjye ni 0793092164"))
# Output: "Nimero yanjye ni zeru karindwi icyenda gatatu zeru icyenda kabiri rimwe gatandatu kane"

print(verbalizer.normalize("Mfite 2345"))     # a plain quantity is untouched
# Output: "Mfite ibihumbi bibiri na magana atatu na mirongo ine na gatanu"
```

| `read_digits` | behaviour |
|---|---|
| `"auto"` (default) | digit by digit only when the token has a leading zero |
| `"always"` | every numeric token digit by digit |
| `"never"` | every numeric token as a cardinal, leading zero included |

A leading zero is an unambiguous signal, so `"auto"` is safe to leave on. A
phone number written without one (`250793092164`) needs a length cut-off
instead, which is off by default because the right value is corpus-specific:

```python
KinyarwandaVerbalizer(digit_threshold=7).normalize("250793092164")
# "kabiri gatanu zeru karindwi icyenda gatatu zeru icyenda kabiri rimwe gatandatu kane"
```

Digits take the counting series and are juxtaposed with no linking `na` -- a
digit sequence is a list, not a sum. Currency, time and date amounts are
unaffected; the option applies only to bare numbers.

### Inline control tags

TTS front-ends carry inline markup in square brackets -- OmniVoice uses
`[laughter]` for non-verbal tags and `[B EY1 S]` for CMU pronunciation
overrides. That markup is not speech, so bracketed spans are held out of
normalization and re-inserted verbatim; a stress digit or a bracketed count
is never read aloud.

```python
verbalizer.normalize("Mfite 12 [laughter] amafaranga")
# "Mfite cumi na kabiri [laughter] amafaranga"

verbalizer.normalize("The [B EY1 S] guitar.")   # unchanged
```

Pass `protect_brackets=False` to normalize inside brackets too.

### Use with a TTS model

The verbalizer is a plain text-to-text function, so it goes in front of any
model without patching it. With OmniVoice:

```python
from verbalizer import KinyarwandaVerbalizer

rw = KinyarwandaVerbalizer()
audio = model.generate(text=rw.normalize(text), language="rw")
```

Different sequences can take different settings -- a year is a quantity, an
account number is not:

```python
quantity = KinyarwandaVerbalizer(read_digits="never")
identifier = KinyarwandaVerbalizer(read_digits="always")

quantity.normalize("Yavutse mu 2006")      # "... ibihumbi bibiri na gatandatu"
identifier.normalize("Konti yawe ni 122006")  # "... rimwe kabiri kabiri zeru zeru gatandatu"
```

## API Reference

### SwahiliVerbalizer / KinyarwandaVerbalizer

Main classes for Swahili and Kinyarwanda text normalization. Both expose the
same interface.

#### Methods

- `normalize(text)`: Apply all normalizations to text, preserving bracketed
  control tags
- `normalize_numbers(text)`: Normalize only numbers
- `normalize_currency(text)`: Normalize only currency
- `normalize_time(text)`: Normalize only time expressions
- `normalize_dates(text)`: Normalize only dates

## Project Structure

```
text-verbalizer/
├── verbalizer/
│   ├── __init__.py
│   ├── base.py              # Abstract base class
│   ├── detector.py          # Pattern detection utilities
│   └── languages/
│       └── swahili/
│           ├── __init__.py
│           ├── config.py    # Regex patterns
│           ├── numbers.py   # Number verbalization
│           ├── currency.py  # Currency verbalization
│           ├── time.py      # Time verbalization
│           └── date.py      # Date verbalization
├── tests/
│   └── test_swahili.py
├── setup.py
├── requirements.txt
└── README.md
```

## CLI

```bash
verbalize                            # interactive REPL
verbalize -l rw "Mfite 2345"         # one-shot
cat lines.txt | verbalize -l sw      # one line in, one line out
```

REPL commands: `:sw` / `:rw` switch language, `:digits auto|always|never`
switches digit reading, `:demo` runs a sample sweep, `:show <text>` prints each
normalizer stage separately, `:q` exits.

`--digits` and `--digit-threshold` set the digit-reading options from the
command line, and `--stages` is the non-interactive form of `:show`.

## Testing

Run tests with pytest:

```bash
pytest tests/
```

Run tests with coverage:

```bash
pytest --cov=verbalizer tests/
```

## Adding New Languages

To add support for a new language:

1. Create a new directory under `verbalizer/languages/[language_name]/`
2. Implement the required modules:
   - `config.py`: Define regex patterns
   - `numbers.py`: Implement number verbalization
   - `currency.py`: Implement currency verbalization
   - `time.py`: Implement time verbalization
   - `date.py`: Implement date verbalization
3. Create a verbalizer class that inherits from `BaseNormalizer`
4. Add tests in `tests/test_[language_name].py`

## Roadmap

- [x] Complete Swahili implementation
- [x] Add Kinyarwanda support
- [ ] Add Hausa support
- [ ] Add Yoruba support
- [ ] Add more currency types