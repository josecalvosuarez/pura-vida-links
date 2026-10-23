---
description: "Task list for feature 001-short-links"
---

# Tasks: Short Links

**Input**: Design documents from `/specs/001-short-links/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml

**Tests**: Required by the constitution (Principle II — Test-First). Tests in each phase are written first and must fail before implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 = Shorten, US2 = Follow, US3 = Custom alias

## Phase 1: Setup

- [ ] T001 Create `src/links/` and `tests/{unit,contract,integration}/` per plan.md
- [ ] T002 Create `pyproject.toml` with FastAPI, Uvicorn, Pydantic; dev extras pytest, httpx, pyyaml
- [ ] T003 [P] Add `tests/conftest.py` with a `client` fixture backed by a temp SQLite file

---

## Phase 2: Foundational (blocks all stories)

- [ ] T004 [P] Unit tests for URL rules in `tests/unit/test_validation.py` (FR-002, FR-011)
- [ ] T005 [P] Unit tests for code generator in `tests/unit/test_codes.py` (FR-003, FR-012, SC-004)
- [ ] T006 [P] Implement `src/links/validation.py` — `validate_url`, `normalize_alias`, `RESERVED`
- [ ] T007 [P] Implement `src/links/codes.py` — `generate_code(length=7)`
- [ ] T008 Implement `src/links/storage.py` — `LinkStore` with `init`, `insert`, `get` (FR-010)
- [ ] T009 Implement `src/links/logging.py` JSON formatter and `GET /health` in `src/links/api.py` (FR-009)

**Checkpoint**: `pytest tests/unit` green.

---

## Phase 3: User Story 1 — Shorten a URL (P1) 🎯 MVP

- [ ] T010 [P] [US1] Contract test `POST /links` 201/422 shapes in `tests/contract/test_links_contract.py`
- [ ] T011 [P] [US1] Integration tests for scenarios 1.1–1.3 in `tests/integration/test_us1_shorten.py`
- [ ] T012 [US1] Implement `POST /links` (random code path) in `src/links/api.py` (FR-001, FR-002, FR-003)

**Checkpoint**: US1 independently demoable.

---

## Phase 4: User Story 2 — Follow a short link (P1)

- [ ] T013 [P] [US2] Integration tests for scenarios 2.1–2.2 in `tests/integration/test_us2_follow.py`
- [ ] T014 [US2] Implement `GET /{code}` → 307 / 404 in `src/links/api.py` (FR-004, FR-005)

---

## Phase 5: User Story 3 — Custom alias (P2)

- [ ] T015 [P] [US3] Integration tests for scenarios 3.1–3.3 + reserved words in `tests/integration/test_us3_alias.py`
- [ ] T016 [US3] Add alias path to `POST /links`; map duplicate key → 409 (FR-006, FR-007, FR-008)

---

## Phase 6: Polish

- [ ] T017 [P] Contract test: every path/method in `contracts/openapi.yaml` exists in the live app schema
- [ ] T018 [P] Update `README.md` with run instructions from quickstart.md
- [ ] T019 Run quickstart.md end-to-end

## Dependencies

- Phase 1 → Phase 2 → (US1 ‖ US2) → US3 → Polish
- US2 tests need a link to exist, so they create one through the API (no hidden coupling to US1 code).

## Parallel example

```text
T004, T005, T006, T007  # four different files, no shared state
```
