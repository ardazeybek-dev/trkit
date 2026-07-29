import pytest

from trkit import is_valid_iban, is_valid_tckn


def make_tckn(first_nine: str) -> str:
    """Build a valid TCKN by computing the check digits for the given 9 digits.

    An independent reference implementation for the tests: it compares the
    validator against the definition of the algorithm rather than against its
    own logic.
    """
    d = [int(c) for c in first_nine]
    tenth = (sum(d[0::2]) * 7 - sum(d[1::2])) % 10
    eleventh = (sum(d) + tenth) % 10
    return first_nine + str(tenth) + str(eleventh)


def test_valid_tckn():
    assert is_valid_tckn("10000000146")


def test_valid_tckn_accepts_int():
    assert is_valid_tckn(10000000146)


def test_valid_tckn_strips_whitespace():
    assert is_valid_tckn("  10000000146  ")


@pytest.mark.parametrize(
    "first_nine",
    ["123456789", "987654321", "100000001", "555555555", "246813579"],
)
def test_generated_tckn_is_valid(first_nine):
    assert is_valid_tckn(make_tckn(first_nine))


@pytest.mark.parametrize(
    ("number", "reason"),
    [
        ("", "empty"),
        ("1234567890", "10 digits"),
        ("123456789012", "12 digits"),
        ("0123456789", "starts with zero"),
        ("01234567890", "starts with zero, 11 digits"),
        ("1234567890a", "contains a letter"),
        ("11111111111", "check digit does not match"),
        ("10000000148", "last digit wrong"),
        ("10000000156", "tenth digit wrong"),
        ("١٢٣٤٥٦٧٨٩٠١", "non-ASCII digits"),
    ],
)
def test_invalid_tckn(number, reason):
    assert not is_valid_tckn(number), reason


def test_generated_tckn_invalid_when_last_digit_corrupted():
    valid = make_tckn("123456789")
    corrupted = valid[:-1] + str((int(valid[-1]) + 1) % 10)
    assert is_valid_tckn(valid)
    assert not is_valid_tckn(corrupted)


def test_valid_iban():
    assert is_valid_iban("TR33 0006 1005 1978 6457 8413 26")


def test_valid_iban_without_spaces():
    assert is_valid_iban("TR330006100519786457841326")


def test_valid_iban_lower_case():
    assert is_valid_iban("tr330006100519786457841326")


@pytest.mark.parametrize(
    ("number", "reason"),
    [
        ("", "empty"),
        ("TR33 0006 1005 1978 6457 8413 27", "check digits do not match"),
        ("TR3300061005197864578413", "24 characters, too short"),
        ("TR3300061005197864578413260", "27 characters, too long"),
        ("DE89370400440532013000", "not a TR IBAN"),
        ("TRXX0006100519786457841326", "check digits are not numeric"),
        ("TR33000610051978645784132X", "letter in the body"),
    ],
)
def test_invalid_iban(number, reason):
    assert not is_valid_iban(number), reason


def test_iban_catches_adjacent_digit_transposition():
    """Why mod-97 exists: it catches two adjacent digits being swapped."""
    valid = "TR330006100519786457841326"
    digits = list(valid)
    assert digits[6] != digits[7], "digits must differ for this test to mean anything"
    digits[6], digits[7] = digits[7], digits[6]

    assert is_valid_iban(valid)
    assert not is_valid_iban("".join(digits))
