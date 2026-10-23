"""T011 — User Story 1: Shorten a URL."""


def test_1_1_valid_url_returns_code_and_short_url(make_link):
    r = make_link(url="https://gdg.community.dev/gdg-pura-vida/")
    body = r.json()
    assert r.status_code == 201
    assert len(body["code"]) == 7
    assert body["short_url"] == f"http://sho.rt/{body['code']}"
    assert body["url"] == "https://gdg.community.dev/gdg-pura-vida/"


def test_1_2_invalid_url_has_clear_message(make_link):
    r = make_link(url="hello")
    assert r.status_code == 422
    assert "http" in str(r.json()["detail"]).lower()


def test_1_3_same_url_twice_gives_new_codes(make_link):
    a = make_link(url="https://example.com").json()["code"]
    b = make_link(url="https://example.com").json()["code"]
    assert a != b
