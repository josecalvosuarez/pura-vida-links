# Research: Short Links

## Decision 1 — HTTP framework

- **Decision**: FastAPI
- **Rationale**: Generates OpenAPI from code, so contract tests can compare the live schema with `contracts/openapi.yaml`; Pydantic validation gives 422s for free.
- **Alternatives considered**: Flask (no built-in schema), stdlib `http.server` (too much boilerplate for a demo).

## Decision 2 — Storage

- **Decision**: SQLite through stdlib `sqlite3`, one table, `code` as PRIMARY KEY.
- **Rationale**: Satisfies FR-010 (persistence) with zero infrastructure; the primary key enforces uniqueness (FR-003, FR-007) atomically.
- **Alternatives considered**: In-memory dict (fails FR-010), Redis/Postgres (violates Principle III), SQLAlchemy (unneeded abstraction).

## Decision 3 — Code generation

- **Decision**: `secrets.choice` over 62 alphanumerics, length 7, retry on collision (max 5).
- **Rationale**: 62⁷ ≈ 3.5 × 10¹² codes; collision probability at 10k links is negligible, and the retry loop + PK constraint guarantees SC-004.
- **Alternatives considered**: Sequential IDs + base62 (guessable), hashing the URL (breaks acceptance scenario 1.3 — same URL must yield new codes).

## Decision 4 — Redirect status

- **Decision**: `307 Temporary Redirect`.
- **Rationale**: Browsers do not cache it permanently, so a future "edit link" feature stays possible.
- **Alternatives considered**: `301` (cached forever by browsers), `302` (method may change).

## Decision 5 — Reserved words

- **Decision**: Reject `health`, `docs`, `links`, `openapi.json` as aliases (from clarification).
- **Rationale**: Prevents an alias from shadowing a real route.
