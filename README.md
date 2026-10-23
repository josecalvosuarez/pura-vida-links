# 🌴 Pura Vida Links

A tiny URL shortener built **spec-first** with [GitHub Spec Kit](https://github.com/github/spec-kit) and **Gemini CLI** — demo repo for the GDG Pura Vida talk *"Spec-Driven Development & Agentic Engineering"*.

> The code is the least interesting part of this repo. Read the `specs/` folder and the git tags.

## The SDD trail — one tag per step

| Tag | Command | Artifact |
|---|---|---|
| `step-0-init` | `specify init --integration gemini` | `.specify/`, `.gemini/commands/` |
| `step-1-constitution` | `/speckit.constitution` | `.specify/memory/constitution.md` |
| `step-2-specify` | `/speckit.specify` | `specs/001-short-links/spec.md` |
| `step-3-clarify` | `/speckit.clarify` | spec.md → `## Clarifications` |
| `step-4-plan` | `/speckit.plan` | `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`, `GEMINI.md` |
| `step-5-tasks` | `/speckit.tasks` | `tasks.md` |
| `step-6-analyze` | `/speckit.analyze` | `analysis.md` + remediation |
| `step-7-implement` | `/speckit.implement` | `src/`, `tests/` — 44 tests green |
| `solution-002-click-stats` | second feature, full loop | answer key for the live demo — 49 tests |

```bash
git log --oneline --decorate          # see the whole story
git diff step-2-specify step-3-clarify -- specs/   # what clarification changed
git checkout step-4-plan              # time-travel to any step
```

Exact prompts for every step: [`docs/PROMPTS.md`](docs/PROMPTS.md) · Live demo script: [`docs/DEMO.md`](docs/DEMO.md)

## Run it

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q                               # 44 passed
uvicorn links.api:app --reload          # http://localhost:8000/docs
```

```bash
curl -s -X POST localhost:8000/links -H 'content-type: application/json' \
     -d '{"url":"https://gdg.community.dev/gdg-pura-vida/","alias":"gdg-oct"}'
curl -si localhost:8000/gdg-oct | head -1     # HTTP/1.1 307 Temporary Redirect
```

## Reproduce from scratch with Gemini

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v1.2.3
specify init my-links --integration gemini --extension git
cd my-links && gemini       # then paste the prompts from docs/PROMPTS.md
```

## Layout

```text
.specify/memory/constitution.md   ← project principles (the "non-negotiables")
.gemini/commands/speckit.*.toml   ← slash commands spec-kit installed for Gemini
GEMINI.md                         ← agent context, updated by /speckit.plan
specs/001-short-links/            ← spec → plan → tasks for feature 001
src/links/                        ← implementation (every function cites an FR-xxx)
tests/{unit,contract,integration} ← written before the code
```
