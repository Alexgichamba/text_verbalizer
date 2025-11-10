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
# Output: "Nina shilingi elfu tano na saa ni saa kumi na nne na dakika thelathini tarehe ishirini na tano mwezi wa Desemba mwaka elfu mbili na ishirini na nne"
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
# Output: "Bei ni mia moja na hamsini elfu"
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

## API Reference

### SwahiliVerbalizer

Main class for Swahili text normalization.

#### Methods

- `normalize(text)`: Apply all normalizations to text
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

- [ ] Complete Swahili implementation
- [ ] Add Hausa support
- [ ] Add Kinyarwanda support
- [ ] Add Yoruba support
- [ ] Add more currency types