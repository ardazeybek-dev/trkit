import pytest

from trkit import asciify, lower, slugify, title, upper


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("istanbul", "İSTANBUL"),
        ("ığdır", "IĞDIR"),
        ("çiğdem", "ÇİĞDEM"),
        ("şükrü", "ŞÜKRÜ"),
        ("", ""),
    ],
)
def test_upper(value, expected):
    assert upper(value) == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("İSTANBUL", "istanbul"),
        ("IĞDIR", "ığdır"),
        ("ÇİĞDEM", "çiğdem"),
        ("", ""),
    ],
)
def test_lower(value, expected):
    assert lower(value) == expected


def test_upper_lower_differ_from_builtins():
    """The reason this package exists: the built-ins are wrong for Turkish."""
    assert "istanbul".upper() == "ISTANBUL"
    assert upper("istanbul") == "İSTANBUL"

    assert "IĞDIR".lower() != "ığdır"
    assert lower("IĞDIR") == "ığdır"


def test_lower_does_not_emit_combining_dot():
    """'İ'.lower() yields two code points in Python; ours must yield one."""
    assert len("İ".lower()) == 2
    assert lower("İ") == "i"
    assert len(lower("İ")) == 1


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("izmir kuş cenneti", "İzmir Kuş Cenneti"),
        ("IĞDIR ovası", "Iğdır Ovası"),
        ("tek", "Tek"),
        ("", ""),
    ],
)
def test_title(value, expected):
    assert title(value) == expected


def test_title_preserves_whitespace():
    assert title("a  b") == "A  B"


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Çiğdem Şahin", "Cigdem Sahin"),
        ("ığdır", "igdir"),
        ("İstanbul", "Istanbul"),
        ("Öğütücü", "Ogutucu"),
        ("abc", "abc"),
    ],
)
def test_asciify(value, expected):
    assert asciify(value) == expected


def test_asciify_returns_only_ascii():
    assert asciify("ĞÜŞİÖÇığüşöç").isascii()


@pytest.mark.parametrize(
    ("value", "expected"),
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
def test_slugify(value, expected):
    assert slugify(value) == expected


def test_slugify_keeps_dotless_capital_i():
    """Regression: folding to ASCII before lower-casing dropped 'I' characters."""
    assert slugify("IĞDIR") == "igdir"
    assert slugify("ISPARTA") == "isparta"


def test_slugify_separator():
    assert slugify("Merhaba Dünya", separator="_") == "merhaba_dunya"
    assert slugify("Merhaba Dünya", separator="") == "merhabadunya"


def test_slugify_output_is_url_safe():
    slug = slugify("Ünlü Şarkıcı: 'Böyle Şeyler' (2026)")
    assert slug.isascii()
    assert all(ch.isalnum() or ch == "-" for ch in slug)
    assert not slug.startswith("-")
    assert not slug.endswith("-")
