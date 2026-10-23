<!--
Sync Impact Report
- Version change: template → 1.0.0
- Added principles: I. Spec Is the Source of Truth, II. Test-First, III. Simplicity (YAGNI),
  IV. Contract-Defined Interfaces, V. Observable & Secure by Default
- Added sections: Technology Constraints, Development Workflow
- Templates reviewed: plan-template.md ✅, spec-template.md ✅, tasks-template.md ✅
- Follow-up TODOs: none
-->

# Pura Vida Links Constitution

## Core Principles

### I. Spec Is the Source of Truth

- Every change starts as a written specification in `specs/###-feature/spec.md`.
- Specs describe **what** and **why**; they MUST NOT name frameworks, libraries or databases.
- Code that is not traceable to a requirement (FR-xxx) or task (Txxx) MUST NOT be merged.
- When behavior changes, the spec is updated first, then the code.

### II. Test-First (NON-NEGOTIABLE)

- Tests are written from the acceptance scenarios **before** the implementation.
- Each user story MUST be independently testable and demoable.
- Red → Green → Refactor. A task is not done until its tests pass.

### III. Simplicity (YAGNI)

- Start with the smallest design that satisfies the spec.
- A single deployable service; no microservices, queues, or caches unless a spec demands them.
- Every added dependency or abstraction MUST be justified in `plan.md` → Complexity Tracking.

### IV. Contract-Defined Interfaces

- Every HTTP endpoint is described in `contracts/` (OpenAPI) before it is implemented.
- Contract tests verify status codes and response shapes against the contract.
- Breaking changes to a contract require a new spec and a version bump.

### V. Observable & Secure by Default

- All input is validated at the boundary; invalid input returns a clear 4xx error, never a 500.
- Only `http` and `https` URLs are accepted.
- The service exposes a health endpoint and writes structured (JSON) logs.

## Technology Constraints

- Language: Python 3.11+.
- Storage: embedded, file-based storage is preferred over external servers for this project size.
- The full test suite MUST run locally in under 30 seconds with a single command.

## Development Workflow

1. `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.analyze` → `/speckit.implement`.
2. One feature per branch, named `###-short-name` (e.g. `001-short-links`).
3. Pull requests MUST link the spec and show the test run.
4. `/speckit.analyze` MUST report zero CRITICAL issues before `/speckit.implement`.

## Governance

- This constitution supersedes ad-hoc practices and agent defaults.
- `/speckit.plan` MUST include a Constitution Check gate; violations are documented or the plan is rejected.
- Amendments use semantic versioning: MAJOR for removed/redefined principles, MINOR for additions, PATCH for wording.

**Version**: 1.0.0 | **Ratified**: 2026-10-23 | **Last Amended**: 2026-10-23
