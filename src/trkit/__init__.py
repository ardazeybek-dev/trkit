"""trkit — Turkish text utilities and Türkiye-specific validators."""

from .plates import PLATES, city_from_plate, plate_from_city
from .text import asciify, lower, slugify, title, upper
from .validate import is_valid_iban, is_valid_tckn

__version__ = "0.2.0"

__all__ = [
    "PLATES",
    "__version__",
    "asciify",
    "city_from_plate",
    "is_valid_iban",
    "is_valid_tckn",
    "lower",
    "plate_from_city",
    "slugify",
    "title",
    "upper",
]
