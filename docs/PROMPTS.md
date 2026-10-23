# Prompts used at each step (Gemini CLI)

Every artifact in this repo was produced by one slash command. These are the exact inputs.
Run `gemini` in the repo root; spec-kit registered the commands in `.gemini/commands/`.

## Step 0 — bootstrap (terminal)

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.3
specify init pura-vida-links --integration gemini --extension git
cd pura-vida-links && gemini
```

## Step 1 — `/speckit.constitution`

```text
/speckit.constitution Create principles for a small, community-run web service:
spec is the source of truth, test-first is non-negotiable, keep it simple (YAGNI, one
service, no external infra), every HTTP endpoint is defined in an OpenAPI contract first,
validate all input and return 4xx not 500, structured JSON logs and a health endpoint.
Python 3.11+, test suite must run in under 30 seconds.
```

## Step 2 — `/speckit.specify`  *(what & why — no tech!)*

```text
/speckit.specify Build a tiny URL shortener for the GDG Pura Vida community. Organizers
paste a long URL (a meetup page, slides, a form) and get a short link they can put on a
slide or a QR code. Anyone who opens the short link is redirected to the original page.
Organizers can optionally choose a memorable alias like gdg-oct.
```

## Step 3 — `/speckit.clarify`

```text
/speckit.clarify
```

Answers given to the agent's questions: no expiry in v1 · aliases 3–32 chars `a-z0-9-` ·
max URL 2,048 · reserved: health, docs, links, openapi.json · random codes 7 alphanumerics.

## Step 4 — `/speckit.plan`  *(now the how)*

```text
/speckit.plan Python 3.11 with FastAPI and Pydantic v2, served by Uvicorn. Store links
in SQLite using the standard-library sqlite3 module, no ORM. Tests with pytest and
FastAPI's TestClient. Single project layout: src/links and tests/{unit,contract,integration}.
```

## Step 5 — `/speckit.tasks`

```text
/speckit.tasks
```

## Step 6 — `/speckit.analyze`

```text
/speckit.analyze
```

Then: *"Apply the remediation for A1, A2 and A3."*

## Step 7 — `/speckit.implement`

```text
/speckit.implement
```
