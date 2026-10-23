"""Random short codes (T007) — FR-003, FR-012. See research.md Decision 3."""
import secrets
import string

ALPHABET = string.ascii_letters + string.digits  # 62 symbols
CODE_LENGTH = 7  # 62^7 ≈ 3.5e12 combinations


def generate_code(length: int = CODE_LENGTH) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
