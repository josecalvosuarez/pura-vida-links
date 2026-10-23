# Feature Specification: Short Links

**Feature Branch**: `001-short-links`

**Created**: 2026-10-23

**Status**: Draft

**Input**: User description: "Build a tiny URL shortener for the GDG Pura Vida community. Organizers paste a long URL (a meetup page, slides, a form) and get a short link they can put on a slide or a QR code. Anyone who opens the short link is redirected to the original page. Organizers can optionally choose a memorable alias like `gdg-oct`."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Shorten a URL (Priority: P1)

An organizer submits a long URL and receives a short code and a full short link they can share.

**Why this priority**: Without creating links there is nothing to share; this is the MVP.

**Independent Test**: Submit a valid URL and confirm a short code is returned; submit an invalid one and confirm a clear error.

**Acceptance Scenarios**:

1. **Given** a valid `https` URL, **When** the organizer submits it, **Then** the system returns a unique short code and the full short link.
2. **Given** a value that is not an `http`/`https` URL (e.g. `ftp://x` or `hello`), **When** it is submitted, **Then** the system rejects it with a validation error explaining why.
3. **Given** the same URL is submitted twice, **When** no alias is requested, **Then** each submission returns a new short code.

---

### User Story 2 - Follow a short link (Priority: P1)

Anyone who opens a short link is sent to the original URL.

**Why this priority**: Sharing is useless if the link does not resolve; it ships together with Story 1.

**Independent Test**: Create a link, request its short path, confirm a redirect to the original URL.

**Acceptance Scenarios**:

1. **Given** an existing short code, **When** a visitor opens it, **Then** they are redirected to the original URL.
2. **Given** an unknown short code, **When** a visitor opens it, **Then** they receive a "not found" response.

---

### User Story 3 - Choose a custom alias (Priority: P2)

An organizer can request a memorable alias (e.g. `gdg-oct`) instead of a random code.

**Why this priority**: Nice for slides and QR codes, but the product works without it.

**Independent Test**: Create a link with an alias, open `/gdg-oct`, confirm redirect; try the same alias again and confirm a conflict error.

**Acceptance Scenarios**:

1. **Given** an unused, valid alias, **When** the organizer requests it, **Then** the short link uses that alias.
2. **Given** an alias already in use, **When** another organizer requests it, **Then** the system reports a conflict and creates nothing.
3. **Given** an alias with invalid characters, **When** it is requested, **Then** the system rejects it with a validation error.

---

### Edge Cases

- What happens when the submitted URL is extremely long?
- What happens when an alias collides with a reserved path such as `health`?
- How long does a short link stay valid? [NEEDS CLARIFICATION: should links expire, and if so after how long?]
- Which characters and lengths are allowed in an alias? [NEEDS CLARIFICATION: alias character set and length limits not specified]

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept a long URL and return a short code plus the full short link.
- **FR-002**: System MUST accept only absolute `http` and `https` URLs.
- **FR-003**: System MUST generate random short codes that are unique across all links.
- **FR-004**: System MUST redirect a visitor from a short code to its original URL.
- **FR-005**: System MUST return a "not found" response for unknown codes.
- **FR-006**: Users MUST be able to request a custom alias for a link.
- **FR-007**: System MUST reject an alias that is already in use with a conflict error.
- **FR-008**: System MUST validate aliases. [NEEDS CLARIFICATION: alias rules]
- **FR-009**: System MUST expose a health check for operators.
- **FR-010**: Links MUST persist across service restarts.

### Key Entities

- **Link**: A mapping from a short code (random or alias) to an original URL, with a creation timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: An organizer can create a short link in a single request, in under 1 second.
- **SC-002**: 100% of invalid URLs and aliases are rejected with a 4xx response and a human-readable message.
- **SC-003**: Redirects resolve in under 100 ms at the 95th percentile on a laptop.
- **SC-004**: Zero duplicate codes after creating 10,000 links in a test run.

## Assumptions

- No user accounts for this version; anyone with network access can create links.
- Click analytics are out of scope (candidate for a future feature).
- The service runs as a single instance.
