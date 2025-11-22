# MemVra Project Log Book

This log captures notable changes, decisions, tests, and outcomes across the MemVra codebase. Use it to maintain continuity, share context, and support compliance and audit needs.

## Conventions
- Date: ISO 8601 (`YYYY-MM-DD`)
- Category: Code | Build | Docs | Infra | Testing | Planning
- Include files changed, commands run (if any), results, and follow-ups

---

### 2025-11-16 — SDK Verification Added
- Category: Code
- Summary: Implemented client-side `verify(factId, secretKey)` in the Java SDK to recompute HMAC and compare with server signature.
- Files Changed:
  - `memvra-client-java/src/main/java/com/memvra/client/MemVraClient.java`
- Result: Agents can now programmatically verify facts before acting.
- Follow-ups: Add SDK builder, timeouts, retry logic, and error mapping.

### 2025-11-16 — Global JSON Error Handling
- Category: Code
- Summary: Introduced a global exception handler to standardize JSON error responses and updated 404 handling.
- Files Changed:
  - `src/main/java/com/memvra/model/ErrorResponse.java`
  - `src/main/java/com/memvra/controller/GlobalExceptionHandler.java`
  - `src/main/java/com/memvra/controller/FactController.java` (404 response)
- Result: Consistent error surface (422 validation, 400 bad JSON, 404 not found).
- Follow-ups: Document error catalog in OpenAPI and README.

### 2025-11-16 — Actuator Health Enabled
- Category: Infra
- Summary: Enabled Spring Boot Actuator health/info endpoints and configured exposure.
- Files Changed:
  - `build.gradle`
  - `src/main/resources/application.yml`
- Result: `/actuator/health` and `/actuator/info` available with sensible defaults.
- Follow-ups: Add metrics and Prometheus integration (Phase 2).

### 2025-11-16 — TestContainers Integration Test
- Category: Testing
- Summary: Added an end-to-end test that records and fetches a fact, recomputes HMAC locally, and asserts signature equality.
- Files Changed:
  - `src/test/java/com/memvra/integration/FactApiIntegrationTest.java`
- Result: Validates cryptographic integrity against a real Postgres container.
- Commands: `gradle test`
- Follow-ups: Expand integration tests for validation errors and edge cases.

### 2025-11-16 — Roadmap Created and Refined
- Category: Planning
- Summary: Authored `roadmap.md` and incorporated feedback (Adoption Layer, freshness, compliance, risk heuristics).
- Files Changed:
  - `roadmap.md`
- Result: Clear phases: Phase 1 (Truth), 1.5 (Adoption), 2 (Operationalization + Freshness), 3 (Intelligence Layer).
- Follow-ups: Ship `v0.1.1` with OpenAPI + SDK ergonomics.

### 2025-11-16 — PDF Extraction Utility
- Category: Docs | Build
- Summary: Added a PDF extractor using PDFBox and Gradle task to parse the strategy PDF for alignment.
- Files Changed:
  - `build.gradle` (task `extractPdf`)
  - `src/main/java/com/memvra/util/PdfExtractor.java`
- Result: Extracted text into `build/pdf/extracted.txt` and printed excerpt.
- Commands: `gradle extractPdf`
- Follow-ups: Optional: keep extracted text synced with roadmap updates.

### 2025-11-15 — Build Fix (commons-codec Coordinates)
- Category: Build
- Summary: Corrected dependency coordinates for `commons-codec` (group `commons-codec`).
- Files Changed:
  - `build.gradle`
- Result: Project builds successfully; prior resolution error fixed.
- Follow-ups: None.

---

### 2025-11-16 — OpenAPI Security + Docs + CI Docker Build
- Category: API | Docs | CI
- Summary: Introduced Swagger `ApiKeyAuth` scheme using header `X-API-Key`, marked `FactController` POST/GET endpoints with security requirements, updated README with Swagger Authorize instructions and `curl` headers, and added a CI job to build the Docker image.
- Files Changed:
  - `src/main/java/com/memvra/config/OpenApiConfig.java`
  - `src/main/java/com/memvra/controller/FactController.java`
  - `README.md`
  - `.github/workflows/ci.yml`
- Commits:
  - `1e1ed77` — ci: add docker-build job to validate Dockerfile on push/PR
  - `418138d` — docs: add Swagger Authorize instructions and include X-API-Key in curl examples
  - `825a5e1` — docs(openapi): mark POST/GET facts endpoints as secured with ApiKeyAuth
  - `6fb9f3e` — docs(openapi): declare ApiKeyAuth scheme (header X-API-Key) in Swagger
- Result:
  - Tests pass (`gradle test`).
  - App runs on `8081`; Swagger UI shows `Authorize` with `ApiKeyAuth` and endpoint security.
  - CI validates Dockerfile builds on push/PR.
- Commands:
  - `gradle test`
  - `gradle bootRun --args='--server.port=8081'`
- Follow-ups:
  - Add API key validation filter/interceptor for 401 handling and metrics.
  - Optional: CI smoke test hitting `/actuator/health` post-boot.

## How to Append New Entries
1. Use the conventions above.
2. Prefer succinct, high-signal summaries.
3. Include any commands run and outcomes (success/warnings/failures).
4. Add follow-ups if the change introduces next tasks.

> Tip: Keep this log updated during significant PRs, releases, and infra changes to support traceability and audits.