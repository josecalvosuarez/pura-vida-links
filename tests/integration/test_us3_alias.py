"""T015 + T020 — User Story 3: Custom alias."""
import pytest


def test_3_1_alias_is_used(client, make_link):
    r = make_link(url="https://example.com/slides", alias="gdg-oct")
    assert r.status_code == 201
    assert r.json()["short_url"] == "http://sho.rt/gdg-oct"
    assert client.get("/gdg-oct").headers["location"] == "https://example.com/slides"


def test_3_2_duplicate_alias_conflicts_and_creates_nothing(client, make_link):
    make_link(url="https://first.example", alias="gdg-oct")
    r = make_link(url="https://second.example", alias="gdg-oct")
    assert r.status_code == 409
    assert client.get("/gdg-oct").headers["location"] == "https://first.example"


@pytest.mark.parametrize("alias", ["a", "has space", "-start", "health", "docs"])
def test_3_3_invalid_or_reserved_alias_is_422(make_link, alias):
    assert make_link(alias=alias).status_code == 422


def test_alias_lookup_is_case_insensitive(client, make_link):
    """FR-013 / analysis A1."""
    make_link(url="https://example.com", alias="GDG-Oct")
    assert client.get("/GDG-OCT").status_code == 307


def test_random_codes_stay_case_sensitive(client, make_link):
    """FR-013 / analysis A1 — exact match wins, lowercase is only a fallback."""
    code = make_link().json()["code"]
    while code == code.lower():  # need a code with at least one uppercase letter
        code = make_link().json()["code"]
    assert client.get(f"/{code}").status_code == 307
    assert client.get(f"/{code.lower()}").status_code == 404
