import pytest
from typer.testing import CliRunner

from trkit import __version__
from trkit.cli import app

runner = CliRunner()


def run(*args):
    return runner.invoke(app, list(args))


def test_version():
    result = run("--version")
    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_no_arguments_shows_help():
    result = run()
    assert "Usage" in result.stdout


def test_slug():
    result = run("slug", "Çığır Açan Şeyler")
    assert result.exit_code == 0
    assert result.stdout.strip() == "cigir-acan-seyler"


def test_slug_separator_option():
    result = run("slug", "Merhaba Dünya", "--separator", "_")
    assert result.stdout.strip() == "merhaba_dunya"


def test_slug_separator_short_option():
    result = run("slug", "Merhaba Dünya", "-s", "_")
    assert result.stdout.strip() == "merhaba_dunya"


@pytest.mark.parametrize(
    ("command", "value", "expected"),
    [
        ("upper", "istanbul", "İSTANBUL"),
        ("lower", "IĞDIR", "ığdır"),
        ("title", "izmir kuş cenneti", "İzmir Kuş Cenneti"),
        ("ascii", "Çiğdem", "Cigdem"),
    ],
)
def test_text_commands(command, value, expected):
    result = run(command, value)
    assert result.exit_code == 0
    assert result.stdout.strip() == expected


def test_valid_tckn_exits_zero():
    result = run("tckn", "10000000146")
    assert result.exit_code == 0
    assert "valid" in result.stdout


def test_invalid_tckn_exits_one():
    """The exit code must be meaningful so the tool works in shell scripts."""
    result = run("tckn", "11111111111")
    assert result.exit_code == 1
    assert "invalid" in result.stdout


def test_valid_iban_exits_zero():
    result = run("iban", "TR33 0006 1005 1978 6457 8413 26")
    assert result.exit_code == 0


def test_invalid_iban_exits_one():
    result = run("iban", "TR33 0006 1005 1978 6457 8413 27")
    assert result.exit_code == 1


def test_plate_code_to_city():
    result = run("plate", "35")
    assert result.exit_code == 0
    assert result.stdout.strip() == "İzmir"


def test_plate_city_to_code():
    result = run("plate", "İzmir")
    assert result.exit_code == 0
    assert result.stdout.strip() == "35"


@pytest.mark.parametrize("value", ["99", "Berlin"])
def test_plate_not_found_is_an_error(value):
    result = run("plate", value)
    assert result.exit_code == 1


def test_plaka_alias_still_works():
    """0.1.0 shipped this command as ``plaka``; the alias must keep working."""
    result = run("plaka", "35")
    assert result.exit_code == 0
    assert result.stdout.strip() == "İzmir"


def test_unknown_command_is_an_error():
    result = run("no-such-command", "x")
    assert result.exit_code != 0
