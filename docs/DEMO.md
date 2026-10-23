# 15-minute demo script

Two acts: **walk the trail** (feature 001, already built — every step is a git tag) and
**go live** (feature 002 with Gemini, with a safety net).

## Before the talk (5 min, at home)

```bash
git clone <this repo> && cd pura-vida-links
make install && make test            # 44 passed
gemini --version                     # signed in, model selected (/model)
git fetch --tags
```

Terminal font ≥ 18 pt · two panes: **left** = editor on `specs/`, **right** = terminal · close Slack.

---

## Act 1 — Walk the trail (≈ 8 min)

| ⏱ | Show | Say |
|---|---|---|
| 0:00 | `git log --oneline --graph --decorate` | "Every commit is one slash command. Code only appears in the last one." |
| 0:45 | `ls .gemini/commands/` | "`specify init --integration gemini` installed these. They are just prompt files (TOML) — open one." |
| 1:30 | `.specify/memory/constitution.md` | "The non-negotiables. Test-first, YAGNI, contracts first. The agent must obey these in every phase." |
| 2:30 | `git show step-2-specify:specs/001-short-links/spec.md` | "What & why only. User stories with priorities, Given/When/Then. Note the two **[NEEDS CLARIFICATION]** markers — the agent refused to guess." |
| 3:30 | `git diff step-2-specify step-3-clarify -- specs/` | "`/speckit.clarify` asked 5 questions; answers are recorded in the spec, not lost in chat." |
| 4:30 | `specs/001-short-links/plan.md` → Constitution Check table | "Now the **how**. Plan is gated by the constitution." |
| 5:15 | `contracts/openapi.yaml`, `research.md` Decision 4 | "Decisions with rejected alternatives — this is your ADR for free." |
| 6:00 | `tasks.md` | "Ordered, `[P]` = parallel-safe, tests before code, grouped by user story → each story is an MVP slice." |
| 6:45 | `analysis.md` row **A1** | "The best moment: `/speckit.analyze` caught a real bug *before any code* — case-insensitive aliases vs case-sensitive codes." |
| 7:30 | `make test` → `src/links/api.py` comments `# FR-013` | "44 green. Every function cites the requirement it implements. Traceability end-to-end." |

## Act 2 — Go live: feature 002 "Click Stats" (≈ 6 min)

```bash
gemini
```

```text
/speckit.specify Organizers want to know if people actually used the link on their slide.
Count how many times each short link was opened and when it was last opened, and let
organizers look that up.
```

→ Point out: new branch `002-…`, new folder `specs/002-…/`, spec has no tech words.

```text
/speckit.clarify
```

Suggested answers: *every redirect counts, no de-dup* · *anyone with the code can read stats*.

```text
/speckit.plan Same stack as 001. No new dependencies. Add clicks and last_clicked_at
columns to the links table with an idempotent migration so existing links report 0.
New endpoint GET /links/{code}/stats.
```

```text
/speckit.tasks
/speckit.implement
```

Then `make test`.

### 🛟 Safety net (Wi-Fi dies, quota hits, agent wanders)

```bash
git stash -u      # park whatever Gemini produced
git log --oneline step-7-implement..solution-002-click-stats   # 5 commits: spec → plan → tasks → RED → GREEN
git checkout solution-002-click-stats
make test         # 49 passed
```

Highlight the commit `failing tests first — RED` → then `GREEN`. That's Principle II in the history.

## Act 3 — Close (≈ 1 min)

```bash
make run          # http://localhost:8000/docs
curl -s -X POST localhost:8000/links -H 'content-type: application/json' \
     -d '{"url":"https://gdg.community.dev/gdg-pura-vida/","alias":"gdg-pv"}'
```

Open `http://localhost:8000/gdg-pv` in the browser → lands on the GDG page. 🎤
