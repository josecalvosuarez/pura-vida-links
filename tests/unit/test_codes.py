"""T005 — random code generator (FR-003, FR-012, SC-004)."""
import re

from links.codes import generate_code


def test_code_is_seven_alphanumerics():
    assert re.fullmatch(r"[A-Za-z0-9]{7}", generate_code())


def test_ten_thousand_codes_are_unique():
    codes = {generate_code() for _ in range(10_000)}
    assert len(codes) == 10_000
