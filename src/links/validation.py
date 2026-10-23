"""Pure validation rules (T006). No HTTP, no storage — easy to unit test."""
import re
from urllib.parse import urlparse

MAX_URL_LENGTH = 2048  # FR-011
RESERVED = frozenset({"health", "docs", "links", "openapi.json"})  # Clarification 2026-10-23
ALIAS_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{2,31}$")  # FR-008


class ValidationError(ValueError):
    """Raised when user input breaks a spec rule."""


def validate_url(url: str) -> str:
    """FR-002 + FR-011: absolute http(s) URL, at most 2048 characters."""
    if len(url) > MAX_URL_LENGTH:
        raise ValidationError(f"URL must be at most {MAX_URL_LENGTH} characters")
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValidationError("URL must be an absolute http or https URL")
    return url


def normalize_alias(alias: str) -> str:
    """FR-008: lowercase, 3-32 chars of a-z 0-9 '-', starts alphanumeric, not reserved."""
    value = alias.lower()
    if value in RESERVED:
        raise ValidationError(f"'{value}' is a reserved word")
    if not ALIAS_PATTERN.fullmatch(value):
        raise ValidationError(
            "Alias must be 3-32 characters of a-z, 0-9 or '-', starting with a letter or digit"
        )
    return value
