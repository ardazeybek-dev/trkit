import pytest

from trkit import is_valid_iban, is_valid_tckn


def tckn_uret(ilk_dokuz: str) -> str:
    """Verilen 9 haneye göre kontrol hanelerini hesaplayıp geçerli bir TCKN üretir.

    Testin bağımsız bir referans uygulaması: doğrulayıcıyı kendi mantığıyla
    değil, algoritmanın tanımıyla karşılaştırır.
    """
    d = [int(c) for c in ilk_dokuz]
    onuncu = (sum(d[0::2]) * 7 - sum(d[1::2])) % 10
    on_birinci = (sum(d) + onuncu) % 10
    return ilk_dokuz + str(onuncu) + str(on_birinci)


def test_gecerli_tckn():
    assert is_valid_tckn("10000000146")


def test_gecerli_tckn_int_kabul_eder():
    assert is_valid_tckn(10000000146)


def test_gecerli_tckn_bosluklari_kirpar():
    assert is_valid_tckn("  10000000146  ")


@pytest.mark.parametrize(
    "ilk_dokuz",
    ["123456789", "987654321", "100000001", "555555555", "246813579"],
)
def test_uretilen_tckn_gecerli(ilk_dokuz):
    assert is_valid_tckn(tckn_uret(ilk_dokuz))


@pytest.mark.parametrize(
    ("numara", "sebep"),
    [
        ("", "boş"),
        ("1234567890", "10 hane"),
        ("123456789012", "12 hane"),
        ("0123456789", "sıfırla başlıyor"),
        ("01234567890", "sıfırla başlıyor, 11 hane"),
        ("1234567890a", "harf içeriyor"),
        ("11111111111", "kontrol hanesi tutmuyor"),
        ("10000000148", "son hane yanlış"),
        ("10000000156", "onuncu hane yanlış"),
        ("١٢٣٤٥٦٧٨٩٠١", "ASCII olmayan rakamlar"),
    ],
)
def test_gecersiz_tckn(numara, sebep):
    assert not is_valid_tckn(numara), sebep


def test_uretilen_tcknin_son_hanesi_bozulunca_gecersiz():
    gecerli = tckn_uret("123456789")
    bozuk = gecerli[:-1] + str((int(gecerli[-1]) + 1) % 10)
    assert is_valid_tckn(gecerli)
    assert not is_valid_tckn(bozuk)


def test_gecerli_iban():
    assert is_valid_iban("TR33 0006 1005 1978 6457 8413 26")


def test_gecerli_iban_bosluksuz():
    assert is_valid_iban("TR330006100519786457841326")


def test_gecerli_iban_kucuk_harf():
    assert is_valid_iban("tr330006100519786457841326")


@pytest.mark.parametrize(
    ("numara", "sebep"),
    [
        ("", "boş"),
        ("TR33 0006 1005 1978 6457 8413 27", "kontrol hanesi tutmuyor"),
        ("TR3300061005197864578413", "24 hane, kısa"),
        ("TR3300061005197864578413260", "27 hane, uzun"),
        ("DE89370400440532013000", "TR değil"),
        ("TRXX0006100519786457841326", "kontrol hanesi rakam değil"),
        ("TR33000610051978645784132X", "gövdede harf var"),
    ],
)
def test_gecersiz_iban(numara, sebep):
    assert not is_valid_iban(numara), sebep


def test_iban_bitisik_rakam_degisimini_yakalar():
    """mod-97'nin varlık sebebi: yan yana iki rakamın yer değiştirmesini yakalamak."""
    gecerli = "TR330006100519786457841326"
    haneler = list(gecerli)
    assert haneler[6] != haneler[7], "test anlamlı olsun diye haneler farklı olmalı"
    haneler[6], haneler[7] = haneler[7], haneler[6]

    assert is_valid_iban(gecerli)
    assert not is_valid_iban("".join(haneler))
