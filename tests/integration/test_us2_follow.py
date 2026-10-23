"""T013 — User Story 2: Follow a short link."""


def test_2_1_known_code_redirects(client, make_link):
    code = make_link(url="https://example.com/slides").json()["code"]
    r = client.get(f"/{code}")
    assert r.status_code == 307
    assert r.headers["location"] == "https://example.com/slides"


def test_2_2_unknown_code_is_404(client):
    r = client.get("/doesNotExist")
    assert r.status_code == 404
    assert r.json() == {"detail": "Short link not found"}


def test_links_survive_restart(tmp_path):
    """FR-010 — persistence across restarts."""
    from fastapi.testclient import TestClient

    from links.api import create_app

    db = tmp_path / "persist.db"
    with TestClient(create_app(db_path=db)) as c1:
        code = c1.post("/links", json={"url": "https://example.com"}).json()["code"]
    with TestClient(create_app(db_path=db), follow_redirects=False) as c2:
        assert c2.get(f"/{code}").status_code == 307
