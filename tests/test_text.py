import pytest

from trkit import asciify, lower, slugify, title, upper


@pytest.mark.parametrize(
    ("girdi", "beklenen"),
    [
        ("istanbul", "İSTANBUL"),
        ("ığdır", "IĞDIR"),
        ("çiğdem", "ÇİĞDEM"),
        ("şükrü", "ŞÜKRÜ"),
        ("", ""),
    ],
)
def test_upper(girdi, beklenen):
    assert upper(girdi) == beklenen


@pytest.mark.parametrize(
    ("girdi", "beklenen"),
    [
        ("İSTANBUL", "istanbul"),
        ("IĞDIR", "ığdır"),
        ("ÇİĞDEM", "çiğdem"),
        ("", ""),
    ],
)
def test_lower(girdi, beklenen):
    assert lower(girdi) == beklenen


def test_upper_lower_yerlesikten_farkli():
    """Paketin var olma sebebi: yerleşik metotlar Türkçe'de yanlış sonuç verir."""
    assert "istanbul".upper() == "ISTANBUL"
    assert upper("istanbul") == "İSTANBUL"

    assert "IĞDIR".lower() != "ığdır"
    assert lower("IĞDIR") == "ığdır"


def test_lower_birlesik_nokta_uretmez():
    """'İ'.lower() Python'da iki kod noktası üretir; bizim çıktımız tek olmalı."""
    assert len("İ".lower()) == 2
    assert lower("İ") == "i"
    assert len(lower("İ")) == 1


@pytest.mark.parametrize(
    ("girdi", "beklenen"),
    [
        ("izmir kuş cenneti", "İzmir Kuş Cenneti"),
        ("IĞDIR ovası", "Iğdır Ovası"),
        ("tek", "Tek"),
        ("", ""),
    ],
)
def test_title(girdi, beklenen):
    assert title(girdi) == beklenen


def test_title_bosluklari_korur():
    assert title("a  b") == "A  B"


@pytest.mark.parametrize(
    ("girdi", "beklenen"),
    [
        ("Çiğdem Şahin", "Cigdem Sahin"),
        ("ığdır", "igdir"),
        ("İstanbul", "Istanbul"),
        ("Öğütücü", "Ogutucu"),
        ("abc", "abc"),
    ],
)
def test_asciify(girdi, beklenen):
    assert asciify(girdi) == beklenen


def test_asciify_sadece_ascii_dondurur():
    assert asciify("ĞÜŞİÖÇığüşöç").isascii()


@pytest.mark.parametrize(
    ("girdi", "beklenen"),
    [
        ("Çığır Açan Şeyler", "cigir-acan-seyler"),
        ("Merhaba  Dünya!", "merhaba-dunya"),
        ("  boşluklu  ", "bosluklu"),
        ("---çok---tire---", "cok-tire"),
        ("Ürün #42", "urun-42"),
        ("", ""),
        ("!!!", ""),
    ],
)
def test_slugify(girdi, beklenen):
    assert slugify(girdi) == beklenen


def test_slugify_buyuk_i_harfini_kaybetmez():
    """Regresyon: önce ASCII'ye indirgeyip sonra küçültmek 'I' harflerini siliyordu."""
    assert slugify("IĞDIR") == "igdir"
    assert slugify("ISPARTA") == "isparta"


def test_slugify_ayirici():
    assert slugify("Merhaba Dünya", separator="_") == "merhaba_dunya"
    assert slugify("Merhaba Dünya", separator="") == "merhabadunya"


def test_slugify_ciktisi_url_guvenli():
    slug = slugify("Ünlü Şarkıcı: 'Böyle Şeyler' (2026)")
    assert slug.isascii()
    assert all(ch.isalnum() or ch == "-" for ch in slug)
    assert not slug.startswith("-")
    assert not slug.endswith("-")
