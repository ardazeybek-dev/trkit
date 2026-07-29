"""Türkiye'ye özgü doğrulayıcılar: TC kimlik numarası ve IBAN."""

from __future__ import annotations

import re

__all__ = ["is_valid_iban", "is_valid_tckn"]

_TCKN_RE = re.compile(r"\A[1-9][0-9]{10}\Z")
_IBAN_RE = re.compile(r"\ATR[0-9]{2}[0-9]{22}\Z")


def is_valid_tckn(value: str | int) -> bool:
    """TC kimlik numarasının algoritmik olarak geçerli olup olmadığını söyler.

    Kurallar:

    1. 11 hane, tamamı rakam, ilk hane sıfır olamaz.
    2. ``(1., 3., 5., 7., 9. hanelerin toplamı * 7 - 2., 4., 6., 8. hanelerin
       toplamı) mod 10`` 10. haneye eşit olmalıdır.
    3. İlk 10 hanenin toplamının 10'a bölümünden kalan 11. haneye eşit olmalıdır.

    Bu yalnızca matematiksel bir kontroldür; numaranın gerçekten birine ait
    olduğunu göstermez.

    >>> is_valid_tckn("10000000146")
    True
    >>> is_valid_tckn("11111111111")
    False
    """
    text = str(value).strip()
    if not _TCKN_RE.match(text):
        return False

    digits = [int(ch) for ch in text]
    odd_sum = digits[0] + digits[2] + digits[4] + digits[6] + digits[8]
    even_sum = digits[1] + digits[3] + digits[5] + digits[7]

    if (odd_sum * 7 - even_sum) % 10 != digits[9]:
        return False
    return sum(digits[:10]) % 10 == digits[10]


def is_valid_iban(value: str) -> bool:
    """Türkiye IBAN'ının geçerli olup olmadığını söyler.

    Boşluklar yok sayılır. Doğrulama, ISO 13616'daki mod-97 kontrolüdür:
    ilk dört karakter sona taşınır, harfler sayıya çevrilir (A=10 … Z=35) ve
    sonucun 97'ye bölümünden kalan 1 olmalıdır.

    >>> is_valid_iban("TR33 0006 1005 1978 6457 8413 26")
    True
    >>> is_valid_iban("TR33 0006 1005 1978 6457 8413 27")
    False
    """
    compact = re.sub(r"\s+", "", str(value)).upper()
    if not _IBAN_RE.match(compact):
        return False

    rearranged = compact[4:] + compact[:4]
    numeric = "".join(str(int(ch, 36)) if ch.isalpha() else ch for ch in rearranged)
    return int(numeric) % 97 == 1
