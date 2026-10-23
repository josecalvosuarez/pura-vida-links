"""Shared fixtures (T003)."""
import pytest
from fastapi.testclient import TestClient

from links.api import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(db_path=tmp_path / "test.db", base_url="http://sho.rt")
    with TestClient(app, follow_redirects=False) as c:
        yield c


@pytest.fixture
def make_link(client):
    def _make(url="https://gdg.community.dev/gdg-pura-vida/", alias=None):
        body = {"url": url}
        if alias is not None:
            body["alias"] = alias
        return client.post("/links", json=body)

    return _make
