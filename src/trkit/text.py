"""Türkçe metin işlemleri.

Python'un yerleşik ``str.upper()`` / ``str.lower()`` metotları Türkçe'nin
noktalı/noktasız ``i`` ayrımını bilmez::

    "istanbul".upper()   -> "ISTANBUL"   (yanlış, doğrusu "İSTANBUL")
    "IĞDIR".lower()      -> "iğdır"      (yanlış, doğrusu "ığdır")

Bu modüldeki fonksiyonlar bu dönüşümleri Türkçe kurallarına göre yapar.
"""

from __future__ import annotations

import re
import unicodedata

__all__ = ["asciify", "lower", "slugify", "title", "upper"]

# Küçültmeden önce eşlenmesi gereken harfler. "İ".lower() Python'da iki kod
# noktası ("i" + birleşik nokta) üretir; bu yüzden önce eşliyoruz.
_LOWER_MAP = {"I": "ı", "İ": "i"}

# Büyütmeden önce eşlenmesi gereken harfler.
_UPPER_MAP = {"i": "İ", "ı": "I"}

# Türkçe harflerin ASCII karşılıkları.
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
    """Metni Türkçe kurallarına göre küçük harfe çevirir.

    >>> lower("IĞDIR")
    'ığdır'
    >>> lower("İSTANBUL")
    'istanbul'
    """
    return "".join(_LOWER_MAP.get(ch, ch) for ch in text).lower()


def upper(text: str) -> str:
    """Metni Türkçe kurallarına göre büyük harfe çevirir.

    >>> upper("istanbul")
    'İSTANBUL'
    >>> upper("ığdır")
    'IĞDIR'
    """
    return "".join(_UPPER_MAP.get(ch, ch) for ch in text).upper()


def title(text: str) -> str:
    """Her kelimenin ilk harfini Türkçe kurallarına göre büyütür.

    Kelime ayırıcı boşluklar korunur.

    >>> title("izmir kuş cenneti")
    'İzmir Kuş Cenneti'
    """
    parts = re.split(r"(\s+)", text)
    return "".join(p if p.isspace() else upper(p[:1]) + lower(p[1:]) for p in parts)


def asciify(text: str) -> str:
    """Türkçe harfleri ASCII karşılıklarına çevirir, kalan aksanları atar.

    >>> asciify("Çiğdem Şahin")
    'Cigdem Sahin'
    """
    mapped = "".join(_ASCII_MAP.get(ch, ch) for ch in text)
    decomposed = unicodedata.normalize("NFKD", mapped)
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def slugify(text: str, separator: str = "-") -> str:
    """Metni URL'de kullanılabilir bir slug'a çevirir.

    Türkçe harfler ASCII'ye indirgenir, alfanümerik olmayan her şey
    ``separator`` ile değiştirilir, baştaki/sondaki ve tekrar eden
    ayırıcılar temizlenir.

    >>> slugify("Çığır Açan Şeyler")
    'cigir-acan-seyler'
    >>> slugify("Merhaba  Dünya!", separator="_")
    'merhaba_dunya'
    """
    # Sıra önemli: önce Türkçe küçültme, sonra ASCII'ye indirgeme. Ters sırada
    # "IĞDIR" önce "IGDIR" olur, ardından Türkçe kural "I" harfini "ı" yapar ve
    # ASCII olmadığı için elenir.
    ascii_text = asciify(lower(text)).lower()
    slug = re.sub(r"[^a-z0-9]+", separator, ascii_text)
    if separator:
        slug = slug.strip(separator)
    return slug
