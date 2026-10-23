# pura-vida-links Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-10-23

## Active Technologies

- Python 3.11+ + FastAPI, Pydantic v2, Uvicorn (001-short-links)
- SQLite via stdlib `sqlite3` (001-short-links)

## Project Structure

```text
src/links/
tests/{unit,contract,integration}/
specs/###-feature/
```

## Commands

- `pip install -e ".[dev]"`
- `pytest -q`
- `uvicorn links.api:app --reload`

## Code Style

- Follow `.specify/memory/constitution.md` (spec first, test first, YAGNI).
- Reference the requirement (FR-xxx) in a docstring or comment next to the code that implements it.

## Recent Changes

- 001-short-links: Added create/redirect/alias/health endpoints

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
