# trkit

[![CI](https://github.com/ardazeybek-dev/trkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ardazeybek-dev/trkit/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/trkit.svg)](https://pypi.org/project/trkit/)
[![Python](https://img.shields.io/pypi/pyversions/trkit.svg)](https://pypi.org/project/trkit/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Turkish text utilities and Türkiye-specific validators. Light on dependencies,
fully typed, usable both as a library and as a command line tool.

**[Try it in your browser →](https://trkit-arda.shipstatic.com)**

## Why

Python's built-in string methods do not know about the Turkish dotted/dotless
`i` distinction, so they quietly corrupt city names, personal names and search
queries:

```python
"istanbul".upper()   # 'ISTANBUL'  ← wrong, should be 'İSTANBUL'
"IĞDIR".lower()      # 'iğdir'     ← wrong, should be 'ığdır'
"izmir".title()      # 'Izmir'     ← wrong, should be 'İzmir'
```

`trkit` applies the Turkish casing rules correctly, and adds a few validators
that come up constantly when building software for Türkiye.

## Installation

```bash
pip install trkit
```

Requires Python 3.10 or newer.

## Library usage

```python
from trkit import upper, lower, title, slugify, asciify
from trkit import is_valid_tckn, is_valid_iban
from trkit import city_from_plate, plate_from_city

upper("istanbul")                 # 'İSTANBUL'
lower("IĞDIR")                    # 'ığdır'
title("izmir kuş cenneti")        # 'İzmir Kuş Cenneti'
asciify("Çiğdem Şahin")           # 'Cigdem Sahin'
slugify("Çığır Açan Şeyler")      # 'cigir-acan-seyler'
slugify("Merhaba Dünya", "_")     # 'merhaba_dunya'

is_valid_tckn("10000000146")                       # True
is_valid_iban("TR33 0006 1005 1978 6457 8413 26")  # True

city_from_plate(35)               # 'İzmir'
plate_from_city("İSTANBUL")       # 34
```

## Command line usage

```bash
$ trkit slug "Çığır Açan Şeyler"
cigir-acan-seyler

$ trkit upper istanbul
İSTANBUL

$ trkit plate 35
İzmir

$ trkit plate İzmir
35

$ trkit tckn 10000000146
valid
```

Validation commands return a meaningful exit code (valid → `0`, invalid → `1`),
so they can be used directly in shell scripts:

```bash
if trkit iban "$IBAN" > /dev/null; then
    echo "IBAN accepted"
fi
```

Run `trkit --help` for the full command list.

## API

| Function | Description |
| --- | --- |
| `upper(text)` | Upper-case using Turkish rules |
| `lower(text)` | Lower-case using Turkish rules |
| `title(text)` | Capitalise The First Letter Of Each Word |
| `asciify(text)` | Fold Turkish letters down to ASCII |
| `slugify(text, separator="-")` | Produce a URL-safe slug |
| `is_valid_tckn(value)` | Turkish national ID checksum validation |
| `is_valid_iban(value)` | Türkiye IBAN mod-97 validation |
| `city_from_plate(code)` | Plate code → province name |
| `plate_from_city(city)` | Province name → plate code |
| `PLATES` | `{code: province}` mapping (81 provinces) |

`is_valid_tckn` is a checksum test only; it does not prove that the number is
issued to an actual person.

## Development

```bash
git clone https://github.com/ardazeybek-dev/trkit.git
cd trkit
python -m venv .venv
.venv\Scripts\activate        # Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"

pytest                          # tests
ruff check .                    # lint
ruff format .                   # formatting
```

## Changelog

### 0.2.0

Documentation and the command line interface are now in English, so the project
is usable outside Turkish-speaking teams. **The library API is unchanged.**

- `trkit plaka` is now `trkit plate` — the old name still works as a hidden alias.
- `--ayirici` is now `--separator` (short flag `-s`).
- Validation commands print `valid` / `invalid` instead of `geçerli` / `geçersiz`.
  Exit codes are unchanged, so shell scripts checking the exit status keep working.

### 0.1.0

Initial release.

## License

[MIT](LICENSE) © Arda Zeybek
