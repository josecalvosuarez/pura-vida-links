# Data Model: Short Links

## Entity: Link

| Field | Type | Rules | Source |
|---|---|---|---|
| `code` | text, PK | Random: 7 chars `[A-Za-z0-9]`; Alias: 3–32 chars `[a-z0-9-]`, starts alnum, not reserved, lowercased | FR-003, FR-008, FR-012 |
| `url` | text, not null | Absolute `http`/`https`, ≤ 2,048 chars | FR-002, FR-011 |
| `created_at` | text (ISO-8601 UTC) | Set by server | Spec → Key Entities |

```sql
CREATE TABLE IF NOT EXISTS links (
    code       TEXT PRIMARY KEY,
    url        TEXT NOT NULL,
    created_at TEXT NOT NULL
);
```

## State transitions

`(none) ──POST /links──▶ active` — no expiry in v1 (clarification 2026-10-23).
