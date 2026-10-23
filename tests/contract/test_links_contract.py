"""T010 + T017 — responses and routes match contracts/openapi.yaml (Principle IV)."""
from pathlib import Path

import yaml

CONTRACT = yaml.safe_load(
    (Path(__file__).parents[2] / "specs/001-short-links/contracts/openapi.yaml").read_text()
)


def test_create_link_201_matches_schema(make_link):
    r = make_link()
    assert r.status_code == 201
    required = CONTRACT["components"]["schemas"]["Link"]["required"]
    assert set(required) <= r.json().keys()


def test_invalid_url_is_422(make_link):
    assert make_link(url="ftp://nope").status_code == 422


def test_every_contract_route_exists_in_app(client):
    live = client.get("/openapi.json").json()["paths"]
    for path, methods in CONTRACT["paths"].items():
        assert path in live, f"missing route {path}"
        for method in methods:
            assert method in live[path], f"missing {method.upper()} {path}"
