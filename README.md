# trkit

[![CI](https://github.com/ardazeybek-dev/trkit/actions/workflows/ci.yml/badge.svg)](https://github.com/ardazeybek-dev/trkit/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/trkit.svg)](https://pypi.org/project/trkit/)
[![Python](https://img.shields.io/pypi/pyversions/trkit.svg)](https://pypi.org/project/trkit/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Türkçe metin araçları ve Türkiye'ye özgü doğrulayıcılar. Bağımlılığı hafif, tip
bilgisi tam, hem kütüphane hem komut satırı aracı olarak kullanılabilir.

**[Tarayıcıda dene →](https://trkit-arda.shipstatic.com)**

> *Turkish text utilities and Türkiye-specific validators: locale-correct case
> conversion, slugify, national ID (TCKN) and IBAN validation, licence-plate
> lookup. Usable as a library or a CLI.*

## Neden?

Python'un yerleşik metotları Türkçe'nin noktalı/noktasız `i` ayrımını bilmez:

```python
"istanbul".upper()   # 'ISTANBUL'  ← yanlış
"IĞDIR".lower()      # 'iğdır'     ← yanlış
```

`trkit` bu dönüşümleri doğru yapar ve yanına Türkiye'de sık gereken birkaç
doğrulayıcı ekler.

## Kurulum

```bash
pip install trkit
```

## Kütüphane olarak kullanım

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

## Komut satırından kullanım

```bash
$ trkit slug "Çığır Açan Şeyler"
cigir-acan-seyler

$ trkit upper istanbul
İSTANBUL

$ trkit plaka 35
İzmir

$ trkit plaka İzmir
35

$ trkit tckn 10000000146
geçerli
```

Doğrulama komutları anlamlı çıkış kodu döndürür (geçerli → `0`, geçersiz → `1`),
böylece kabuk betiklerinde doğrudan kullanılabilir:

```bash
if trkit iban "$IBAN" > /dev/null; then
    echo "IBAN kabul edildi"
fi
```

Tüm komutlar için: `trkit --help`

## API

| Fonksiyon | Açıklama |
| --- | --- |
| `upper(text)` | Türkçe kurallarına göre BÜYÜK harf |
| `lower(text)` | Türkçe kurallarına göre küçük harf |
| `title(text)` | Her Kelimenin İlk Harfi Büyük |
| `asciify(text)` | Türkçe harfleri ASCII'ye indirger |
| `slugify(text, separator="-")` | URL'de kullanılabilir slug üretir |
| `is_valid_tckn(value)` | TC kimlik no algoritma kontrolü |
| `is_valid_iban(value)` | Türkiye IBAN mod-97 kontrolü |
| `city_from_plate(code)` | Plaka kodu → il adı |
| `plate_from_city(city)` | İl adı → plaka kodu |
| `PLATES` | `{kod: il}` sözlüğü (81 il) |

`is_valid_tckn` yalnızca matematiksel bir kontroldür; numaranın gerçekten
birine ait olduğunu göstermez.

## Geliştirme

```bash
git clone https://github.com/ardazeybek-dev/trkit.git
cd trkit
python -m venv .venv
.venv\Scripts\activate        # Linux/macOS: source .venv/bin/activate
pip install -e ".[dev]"

pytest                          # testler
ruff check .                    # lint
```

## Lisans

[MIT](LICENSE) © Arda Zeybek
