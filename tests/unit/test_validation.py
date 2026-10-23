"""T004 — URL and alias rules (FR-002, FR-008, FR-011)."""
import pytest

from links.validation import ValidationError, normalize_alias, validate_url


@pytest.mark.parametrize("url", ["https://example.com", "http://example.com/a?b=c#d"])
def test_accepts_http_and_https(url):
    assert validate_url(url) == url


@pytest.mark.parametrize("url", ["ftp://x.com", "hello", "javascript:alert(1)", "https://", ""])
def test_rejects_non_http_urls(url):
    with pytest.raises(ValidationError):
        validate_url(url)


def test_rejects_urls_longer_than_2048():
    with pytest.raises(ValidationError, match="2048"):
        validate_url("https://e.com/" + "a" * 2048)


@pytest.mark.parametrize("raw, expected", [("gdg-oct", "gdg-oct"), ("GDG-Oct", "gdg-oct"), ("a1b", "a1b")])
def test_alias_is_normalized(raw, expected):
    assert normalize_alias(raw) == expected


@pytest.mark.parametrize("alias", ["ab", "-gdg", "gdg_oct", "gdg oct", "x" * 33, "ñandú"])
def test_rejects_bad_alias(alias):
    with pytest.raises(ValidationError):
        normalize_alias(alias)


@pytest.mark.parametrize("alias", ["health", "docs", "links", "openapi.json", "HEALTH"])
def test_rejects_reserved_alias(alias):
    with pytest.raises(ValidationError, match="reserved"):
        normalize_alias(alias)
