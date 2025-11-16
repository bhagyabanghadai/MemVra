# MemVra Roadmap (Phase 1 → Phase 3)

MemVra is a truth-certification layer for AI agents. It records facts with mandatory provenance, signs them with HMAC-SHA256, and stores them immutably for downstream verification.

## Status Snapshot
- Delivered
  - Spring Boot 3.2 service scaffold and Gradle build
  - PostgreSQL schema with Flyway (`fact_records`), indexes
  - Core APIs: `POST /v1/facts`, `GET /v1/facts/{factId}`
  - HMAC-SHA256 signing (`CryptoService`) and Base64 signature
  - Java client SDK (`memvra-client-java`) with `record()` and `verify(factId, secretKey)`
  - Consistent JSON error responses (global handler) and `404 NOT_FOUND` JSON
  - Spring Boot Actuator (`/actuator/health`, `/actuator/info`)
  - TestContainers integration test verifying end-to-end HMAC
  - PDF extraction utility task to keep product aligned with strategy

- In Progress
  - Developer experience (OpenAPI spec, examples) — planned next

- Planned
  - Authentication (API keys) and simple rate limiting
  - Observability and operational hardening (metrics, structured logging)
  - Client SDK ergonomics (builder, timeouts, retry logic, error mapping)
  - Extended capabilities (search/query, batch operations, staleness detection)

## Phase Plan

### Phase 1: Truth Ledger MVP
Goal: Make agents “trust before action” possible via signed facts.

Scope
- Record and retrieve facts with provenance and HMAC signatures
- Immutable storage with indexes for common queries
- Client SDK for record + local verification
- JSON error normalization
- Integration tests with TestContainers
- Basic operational health (Actuator)

Acceptance Criteria
- `POST /v1/facts` returns `201` with `fact_id`, `signature`, `created_at`
- `GET /v1/facts/{factId}` returns complete record or structured `404`
- Client `verify()` recomputes HMAC and matches server signature
- Integration test starts ephemeral Postgres and asserts signature equality
- Health endpoint responds `UP` when service + DB are healthy

Status: Delivered (minor DX/documentation items pending)

### Phase 1.5: Adoption Layer
Goal: Optimize onboarding and integration speed to drive adoption.

Deliverables
- OpenAPI 3.0 spec and interactive docs
- Example requests/responses in README and `examples/`
- Error code catalog (validation, bad request, not found)
- SDK ergonomics: builder, timeouts, retry logic, error mapping
- Optional: `POST /v1/facts/batch` for multi-fact ingest

Acceptance Criteria
- `openapi.yaml` or generated docs available at `/v3/api-docs` and/or static docs
- Examples runnable with `curl` and SDK snippets
- Error responses documented with fields and typical causes
- SDK supports configuration via builder and reasonable retry semantics

Status: Planned (next up)

### Phase 2: Operationalization + Freshness
Goal: Production safety rails, observability, and freshness awareness.

Deliverables
- Authentication (API keys header) and simple rate limiting
- Metrics: request rate, error rate, latency, signature failures
- Structured application logs with correlation IDs
- Config hardening (secret management, environment-driven settings)
- Freshness metadata: `expires_at` and/or `last_verified` on facts
- Audit logging for compliance (SOC 2, HIPAA, GDPR)

Acceptance Criteria
- Requests without valid API key return `401/403` with JSON error
- Rate-limited responses return `429` with retry-after guidance
- Metrics visible via Actuator/Prometheus (if added later)
- Secure secret handling (no dev defaults in prod)
- Fact responses include freshness metadata; stale flags propagate to clients
- Verification and recording events logged for auditability

Status: Planned

### Phase 3: Intelligence Layer
Goal: Insight and control for agents and operators.

Deliverables
- Search and query endpoints (filters + pagination)
- Staleness detection alerts/notifications
- Experimental: Agent Risk Heuristics dashboard (transparent metrics, not a black box)
- Conflict detection/resolution for overlapping facts

Acceptance Criteria
- Query endpoints return paginated results with filters
- Staleness surfaced via alerts or dedicated endpoint
- Risk visibility: heuristics such as % `agent_inference`, failed verifications, staleness rate, conflict frequency
- Operators can identify and triage conflicting records

Status: Planned (post-MVP stabilization)

## Milestones & Ordering
- M0 — MVP compile/build and schema — Delivered
- M1 — Verification pipeline (HMAC + SDK `verify`) — Delivered
- M1.5 — Adoption Layer (OpenAPI, examples, SDK ergonomics, optional batch) — Next
- M2 — Auth & Rate Limiting + Freshness metadata — Planned
- M3 — Observability (metrics, structured logging, audit logging) — Planned
- M4 — Intelligence Layer (search, alerts, risk heuristics, conflict) — Planned

## Release Plan
- `v0.1.0` — Phase 1 MVP (Delivered)
- `v0.1.1` — Phase 1.5 Adoption Layer (Next)
- `v0.2.0` — Phase 2 Operationalization + Freshness
- `v0.3.0` — Phase 3 Intelligence Layer

## Backlog (Prioritized)
1) OpenAPI spec and interactive docs
2) SDK builder + timeouts + retry logic + error mapping
3) Optional: `POST /v1/facts/batch`
4) API key auth + `429` rate limiting
5) Freshness metadata (`expires_at`, `last_verified`)
6) Audit logging for compliance
7) Metrics for signature failures and API latency
8) Structured logs + correlation IDs
9) Query/search endpoint and pagination
10) Risk heuristics dashboard (experimental)
11) Conflict detection/resolution

## Risks & Mitigations
- Secret key exposure — enforce environment-based secrets, avoid dev defaults in prod
- Incomplete validation — continue tightening input constraints and error catalog
- Performance under load — add basic performance tests and monitor latency metrics
- Overreach in Phase 3 — keep scope tight, ship incremental capabilities

## Developer Notes
- Always verify facts client-side before acting (`verify()`)
- Flag `AGENT_INFERENCE` as high-risk; consider policy controls downstream
- Prefer structured logs and consistent error responses for observability
- Include freshness metadata and audit logs to support compliance and safety