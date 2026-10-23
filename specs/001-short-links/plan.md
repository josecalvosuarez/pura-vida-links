# Implementation Plan: Short Links

**Branch**: `001-short-links` | **Date**: 2026-10-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-short-links/spec.md`

## Summary

A single-process HTTP service that stores `code → url` mappings in SQLite and answers
`POST /links` (create), `GET /{code}` (redirect) and `GET /health`. Validation rules
from the clarified spec (URL scheme/length, alias pattern, reserved words) live in one
pure-Python module so they can be unit-tested without HTTP.

## Technical Context

**Language/Version**: Python 3.11+

**Primary Dependencies**: FastAPI (HTTP + OpenAPI), Pydantic v2 (request/response models), Uvicorn (ASGI server)

**Storage**: SQLite via the standard-library `sqlite3` module (single file, `links.db`)

**Testing**: pytest + FastAPI `TestClient` (httpx)

**Target Platform**: Linux/macOS container or laptop

**Project Type**: Single project (web service)

**Performance Goals**: p95 redirect < 100 ms on a laptop (SC-003)

**Constraints**: Full test suite < 30 s (constitution); no external services

**Scale/Scope**: Community tool — thousands of links, tens of requests per second

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Check | Status |
|---|---|---|
| I. Spec is source of truth | Every endpoint maps to FR-001…FR-012 | ✅ |
| II. Test-first | Contract + unit + integration tests precede implementation in tasks.md | ✅ |
| III. Simplicity | One service, stdlib SQLite, no ORM, no cache | ✅ |
| IV. Contract-defined interfaces | `contracts/openapi.yaml` written in Phase 1 | ✅ |
| V. Observable & secure | URL scheme allow-list, 4xx on bad input, `/health`, JSON logs | ✅ |

**Result**: PASS — no violations, Complexity Tracking empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-short-links/
├── plan.md              # This file (/speckit.plan)
├── research.md          # Phase 0 output (/speckit.plan)
├── data-model.md        # Phase 1 output (/speckit.plan)
├── quickstart.md        # Phase 1 output (/speckit.plan)
├── contracts/
│   └── openapi.yaml     # Phase 1 output (/speckit.plan)
├── checklists/
│   └── requirements.md  # Spec quality checklist (/speckit.specify)
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
src/
└── links/
    ├── __init__.py
    ├── validation.py    # Pure rules: URL + alias (FR-002, FR-008, FR-011)
    ├── codes.py         # Random code generator (FR-003, FR-012)
    ├── storage.py       # SQLite repository (FR-010)
    ├── api.py           # FastAPI app + routes (FR-001, FR-004…FR-007, FR-009)
    └── logging.py       # JSON log formatter

tests/
├── unit/                # validation, codes
├── contract/            # responses match openapi.yaml
└── integration/         # user stories end-to-end via TestClient
```

**Structure Decision**: Option 1 (single project). One package, `links`, keeps the
demo readable and satisfies Principle III.

## Complexity Tracking

*No violations — table intentionally empty.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|---|---|---|
