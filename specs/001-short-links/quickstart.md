# Quickstart: Short Links

Validates the feature end-to-end against the acceptance scenarios.

```bash
pip install -e ".[dev]"
uvicorn links.api:app --reload          # http://localhost:8000/docs
```

```bash
# US1 — shorten
curl -s -X POST localhost:8000/links -H 'content-type: application/json' \
     -d '{"url":"https://gdg.community.dev/gdg-pura-vida/"}'
# → 201 {"code":"aB3xK9q","short_url":"http://localhost:8000/aB3xK9q",...}

# US1.2 — invalid scheme
curl -s -X POST localhost:8000/links -H 'content-type: application/json' -d '{"url":"ftp://x"}'
# → 422

# US3 — custom alias, then conflict
curl -s -X POST localhost:8000/links -H 'content-type: application/json' \
     -d '{"url":"https://example.com/slides","alias":"gdg-oct"}'     # → 201
curl -s -X POST localhost:8000/links -H 'content-type: application/json' \
     -d '{"url":"https://example.com/other","alias":"gdg-oct"}'      # → 409

# US2 — follow
curl -si localhost:8000/gdg-oct | head -3      # → 307, Location: https://example.com/slides
curl -si localhost:8000/nope    | head -1      # → 404
```

Run the whole suite: `pytest -q`
