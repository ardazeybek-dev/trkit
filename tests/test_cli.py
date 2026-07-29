import pytest
from typer.testing import CliRunner

from trkit import __version__
from trkit.cli import app

runner = CliRunner()


def calistir(*args):
    return runner.invoke(app, list(args))


def test_version():
    sonuc = calistir("--version")
    assert sonuc.exit_code == 0
    assert sonuc.stdout.strip() == __version__


def test_argumansiz_cagri_yardim_gosterir():
    sonuc = calistir()
    assert "Usage" in sonuc.stdout or "Kullan" in sonuc.stdout


def test_slug():
    sonuc = calistir("slug", "Çığır Açan Şeyler")
    assert sonuc.exit_code == 0
    assert sonuc.stdout.strip() == "cigir-acan-seyler"


def test_slug_ayirici_secenegi():
    sonuc = calistir("slug", "Merhaba Dünya", "--ayirici", "_")
    assert sonuc.stdout.strip() == "merhaba_dunya"


@pytest.mark.parametrize(
    ("komut", "girdi", "beklenen"),
    [
        ("upper", "istanbul", "İSTANBUL"),
        ("lower", "IĞDIR", "ığdır"),
        ("title", "izmir kuş cenneti", "İzmir Kuş Cenneti"),
        ("ascii", "Çiğdem", "Cigdem"),
    ],
)
def test_metin_komutlari(komut, girdi, beklenen):
    sonuc = calistir(komut, girdi)
    assert sonuc.exit_code == 0
    assert sonuc.stdout.strip() == beklenen


def test_gecerli_tckn_cikis_kodu_sifir():
    sonuc = calistir("tckn", "10000000146")
    assert sonuc.exit_code == 0
    assert "geçerli" in sonuc.stdout


def test_gecersiz_tckn_cikis_kodu_bir():
    """Kabuk betiklerinde kullanılabilmesi için çıkış kodu anlamlı olmalı."""
    sonuc = calistir("tckn", "11111111111")
    assert sonuc.exit_code == 1
    assert "geçersiz" in sonuc.stdout


def test_gecerli_iban_cikis_kodu_sifir():
    sonuc = calistir("iban", "TR33 0006 1005 1978 6457 8413 26")
    assert sonuc.exit_code == 0


def test_gecersiz_iban_cikis_kodu_bir():
    sonuc = calistir("iban", "TR33 0006 1005 1978 6457 8413 27")
    assert sonuc.exit_code == 1


def test_plaka_koddan_il():
    sonuc = calistir("plaka", "35")
    assert sonuc.exit_code == 0
    assert sonuc.stdout.strip() == "İzmir"


def test_plaka_ilden_kod():
    sonuc = calistir("plaka", "İzmir")
    assert sonuc.exit_code == 0
    assert sonuc.stdout.strip() == "35"


@pytest.mark.parametrize("deger", ["99", "Berlin"])
def test_plaka_bulunamazsa_hata(deger):
    sonuc = calistir("plaka", deger)
    assert sonuc.exit_code == 1


def test_bilinmeyen_komut_hata_verir():
    sonuc = calistir("boyle-bir-komut-yok", "x")
    assert sonuc.exit_code != 0
