"""Turkish-aware text operations.

Python's built-in ``str.upper()`` / ``str.lower()`` do not know about the
Turkish dotted/dotless ``i`` distinction::

    "istanbul".upper()   -> "ISTANBUL"   (wrong, should be "İSTANBUL")
    "IĞDIR".lower()      -> "iğdır"      (wrong, should be "ığdır")

The functions in this module apply the Turkish rules instead.
"""

from __future__ import annotations

import re
import unicodedata

__all__ = ["asciify", "lower", "slugify", "title", "upper"]

# Letters that must be mapped before lower-casing. In Python "İ".lower()
# produces two code points ("i" + combining dot), so we map it up front.
_LOWER_MAP = {"I": "ı", "İ": "i"}

# Letters that must be mapped before upper-casing.
_UPPER_MAP = {"i": "İ", "ı": "I"}

# ASCII counterparts of the Turkish letters.
# fmt: off
_ASCII_MAP = {
    "ç": "c", "Ç": "C",
    "ğ": "g", "Ğ": "G",
    "ı": "i", "I": "I",
    "İ": "I", "i": "i",
    "ö": "o", "Ö": "O",
    "ş": "s", "Ş": "S",
    "ü": "u", "Ü": "U",
}
# fmt: on


def lower(text: str) -> str:
    """Lower-case text using Turkish rules.

    >>> lower("IĞDIR")
    'ığdır'
    >>> lower("İSTANBUL")
    'istanbul'
    """
    return "".join(_LOWER_MAP.get(ch, ch) for ch in text).lower()


def upper(text: str) -> str:
    """Upper-case text using Turkish rules.

    >>> upper("istanbul")
    'İSTANBUL'
    >>> upper("ığdır")
    'IĞDIR'
    """
    return "".join(_UPPER_MAP.get(ch, ch) for ch in text).upper()


def title(text: str) -> str:
    """Capitalise the first letter of each word using Turkish rules.

    Whitespace between words is preserved.

    >>> title("izmir kuş cenneti")
    'İzmir Kuş Cenneti'
    """
    parts = re.split(r"(\s+)", text)
    return "".join(p if p.isspace() else upper(p[:1]) + lower(p[1:]) for p in parts)


def asciify(text: str) -> str:
    """Replace Turkish letters with ASCII counterparts and drop remaining accents.

    >>> asciify("Çiğdem Şahin")
    'Cigdem Sahin'
    """
    mapped = "".join(_ASCII_MAP.get(ch, ch) for ch in text)
    decomposed = unicodedata.normalize("NFKD", mapped)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def slugify(text: str, separator: str = "-") -> str:
    """Convert text into a URL-safe slug.

    Turkish letters are folded to ASCII, every run of non-alphanumeric
    characters is replaced with ``separator``, and leading, trailing and
    repeated separators are collapsed.

    >>> slugify("Çığır Açan Şeyler")
    'cigir-acan-seyler'
    >>> slugify("Merhaba  Dünya!", separator="_")
    'merhaba_dunya'
    """
    # Order matters: lower-case with Turkish rules first, then fold to ASCII.
    # The other way around, "IĞDIR" would become "IGDIR" first, then the
    # Turkish rule would turn "I" into "ı", which is not ASCII and gets dropped.
    ascii_text = asciify(lower(text)).lower()
    slug = re.sub(r"[^a-z0-9]+", separator, ascii_text)
    if separator:
        slug = slug.strip(separator)
    return slug
