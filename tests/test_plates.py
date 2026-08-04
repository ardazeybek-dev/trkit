import pytest

from trkit import PLATES, city_from_plate, plate_from_city


def test_has_eighty_one_provinces():
    assert len(PLATES) == 81
    assert sorted(PLATES) == list(range(1, 82))


@pytest.mark.parametrize(
    ("code", "city"),
    [(1, "Adana"), (6, "Ankara"), (34, "İstanbul"), (35, "İzmir"), (81, "Düzce")],
)
def test_city_from_code(code, city):
    assert city_from_plate(code) == city


def test_city_from_code_accepts_string_and_leading_zero():
    assert city_from_plate("06") == "Ankara"
    assert city_from_plate(" 35 ") == "İzmir"


@pytest.mark.parametrize("code", [0, 82, 99, -1, "abc", "", "3.5"])
def test_invalid_code_returns_none(code):
    assert city_from_plate(code) is None


@pytest.mark.parametrize(
    ("city", "code"),
    [("İstanbul", 34), ("İSTANBUL", 34), ("istanbul", 34), ("Ankara", 6), ("ığdır", 76)],
)
def test_code_from_city(city, code):
    assert plate_from_city(city) == code


def test_code_from_city_strips_whitespace():
    assert plate_from_city("  İzmir  ") == 35


@pytest.mark.parametrize("city", ["Berlin", "", "  ", "Istanbul-"])
def test_unknown_city_returns_none(city):
    assert plate_from_city(city) is None


def test_round_trip_is_consistent():
    """For every province, code → city → code must return the original value."""
    for code, city in PLATES.items():
        assert plate_from_city(city) == code
        assert city_from_plate(code) == city


def test_city_names_are_unique():
    assert len(set(PLATES.values())) == len(PLATES)
