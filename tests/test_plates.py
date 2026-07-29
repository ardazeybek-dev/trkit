import pytest

from trkit import PLATES, city_from_plate, plate_from_city


def test_seksen_bir_il_var():
    assert len(PLATES) == 81
    assert sorted(PLATES) == list(range(1, 82))


@pytest.mark.parametrize(
    ("kod", "il"),
    [(1, "Adana"), (6, "Ankara"), (34, "İstanbul"), (35, "İzmir"), (81, "Düzce")],
)
def test_koddan_il(kod, il):
    assert city_from_plate(kod) == il


def test_koddan_il_metin_ve_bastaki_sifir():
    assert city_from_plate("06") == "Ankara"
    assert city_from_plate(" 35 ") == "İzmir"


@pytest.mark.parametrize("kod", [0, 82, 99, -1, "abc", "", "3.5"])
def test_gecersiz_kod_none_dondurur(kod):
    assert city_from_plate(kod) is None


@pytest.mark.parametrize(
    ("il", "kod"),
    [("İstanbul", 34), ("İSTANBUL", 34), ("istanbul", 34), ("Ankara", 6), ("ığdır", 76)],
)
def test_ilden_kod(il, kod):
    assert plate_from_city(il) == kod


def test_ilden_kod_bosluklari_kirpar():
    assert plate_from_city("  İzmir  ") == 35


@pytest.mark.parametrize("il", ["Berlin", "", "  ", "Istanbul-"])
def test_bilinmeyen_il_none_dondurur(il):
    assert plate_from_city(il) is None


def test_gidis_donus_tutarli():
    """Her il için kod → il → kod dönüşümü başlangıç değerine dönmeli."""
    for kod, il in PLATES.items():
        assert plate_from_city(il) == kod
        assert city_from_plate(kod) == il


def test_il_adlari_benzersiz():
    assert len(set(PLATES.values())) == len(PLATES)
