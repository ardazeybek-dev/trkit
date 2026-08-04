"""Licence-plate code ↔ province name conversions."""

from __future__ import annotations

from .text import lower

__all__ = ["PLATES", "city_from_plate", "plate_from_city"]

#: Mapping from plate code to province name (1-81).
# fmt: off
PLATES: dict[int, str] = {
    1: "Adana", 2: "Adıyaman", 3: "Afyonkarahisar", 4: "Ağrı", 5: "Amasya",
    6: "Ankara", 7: "Antalya", 8: "Artvin", 9: "Aydın", 10: "Balıkesir",
    11: "Bilecik", 12: "Bingöl", 13: "Bitlis", 14: "Bolu", 15: "Burdur",
    16: "Bursa", 17: "Çanakkale", 18: "Çankırı", 19: "Çorum", 20: "Denizli",
    21: "Diyarbakır", 22: "Edirne", 23: "Elazığ", 24: "Erzincan", 25: "Erzurum",
    26: "Eskişehir", 27: "Gaziantep", 28: "Giresun", 29: "Gümüşhane", 30: "Hakkâri",
    31: "Hatay", 32: "Isparta", 33: "Mersin", 34: "İstanbul", 35: "İzmir",
    36: "Kars", 37: "Kastamonu", 38: "Kayseri", 39: "Kırklareli", 40: "Kırşehir",
    41: "Kocaeli", 42: "Konya", 43: "Kütahya", 44: "Malatya", 45: "Manisa",
    46: "Kahramanmaraş", 47: "Mardin", 48: "Muğla", 49: "Muş", 50: "Nevşehir",
    51: "Niğde", 52: "Ordu", 53: "Rize", 54: "Sakarya", 55: "Samsun",
    56: "Siirt", 57: "Sinop", 58: "Sivas", 59: "Tekirdağ", 60: "Tokat",
    61: "Trabzon", 62: "Tunceli", 63: "Şanlıurfa", 64: "Uşak", 65: "Van",
    66: "Yozgat", 67: "Zonguldak", 68: "Aksaray", 69: "Bayburt", 70: "Karaman",
    71: "Kırıkkale", 72: "Batman", 73: "Şırnak", 74: "Bartın", 75: "Ardahan",
    76: "Iğdır", 77: "Yalova", 78: "Karabük", 79: "Kilis", 80: "Osmaniye",
    81: "Düzce",
}
# fmt: on

# Reverse mapping from province name to plate code. Keys are lower-cased with
# Turkish rules so "istanbul", "İSTANBUL" and "İstanbul" all resolve the same.
_BY_CITY: dict[str, int] = {lower(city): code for code, city in PLATES.items()}


def city_from_plate(code: int | str) -> str | None:
    """Return the province name for a plate code, or ``None`` if invalid.

    >>> city_from_plate(35)
    'İzmir'
    >>> city_from_plate("06")
    'Ankara'
    >>> city_from_plate(99) is None
    True
    """
    try:
        number = int(str(code).strip())
    except ValueError:
        return None
    return PLATES.get(number)


def plate_from_city(city: str) -> int | None:
    """Return the plate code for a province name, or ``None`` if not found.

    Case-insensitive.

    >>> plate_from_city("İSTANBUL")
    34
    >>> plate_from_city("Ankara")
    6
    >>> plate_from_city("Berlin") is None
    True
    """
    return _BY_CITY.get(lower(city.strip()))
