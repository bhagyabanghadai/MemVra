# MemVra Truth Ledger

MemVra is a Spring Boot service that certifies "facts" via mandatory provenance and HMAC-SHA256 signatures stored in an immutable PostgreSQL ledger. Agents use the SDK to verify facts locally before taking actions.

## Status
- Phase 1 (MVP): Delivered
  - APIs: POST `/v1/facts`, GET `/v1/facts/{factId}`
  - HMAC-SHA256 signing and Base64 signature
  - Java client SDK (`memvra-client-java`) with `record()` and `verify(factId, secretKey)`
  - Global JSON error handling (422 validation, 400 bad JSON, structured 404)
  - Spring Boot Actuator: `/actuator/health`, `/actuator/info`
  - Integration test (TestContainers + Postgres) verifies end-to-end HMAC
  - Roadmap and project logbook maintained in repo

## Tech Stack
- Java 17, Spring Boot 3.2
- Gradle build
- PostgreSQL + Flyway
- TestContainers (integration tests)

## Getting Started
1. Ensure Java 17+ and Gradle 8+ installed.
2. Start a local PostgreSQL (example with Docker):
   ```bash
   docker run --rm -e POSTGRES_DB=memvra -e POSTGRES_USER=memvra -e POSTGRES_PASSWORD=password -p 5432:5432 postgres:15
   ```
3. Set environment variable for HMAC key (change in real env):
   - `MEMVRA_SECRET_KEY` (e.g., a 32+ character random string)
4. Build and run:
   ```bash
   gradle bootRun
   ```
5. Health check:
   ```bash
   curl http://localhost:8080/actuator/health
   ```

## API Examples
Record a fact:
```bash
curl -X POST http://localhost:8080/v1/facts \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Customer reported card as stolen",
    "source_type": "user_input",
    "source_id": "chat:session_xyz:turn_5",
    "recorded_by": "agent-support-bot-v2"
  }'
```

Retrieve a fact:
```bash
curl -X GET http://localhost:8080/v1/facts/{fact_id}
```

## SDK Usage (Java)
```java
MemVraClient client = new MemVraClient("http://localhost:8080", "test-key");
Fact fact = new Fact("Test fact")
    .withSource(SourceType.USER_INPUT, "test:source:1")
    .recordedBy("test-agent");

Map<?,?> record = client.record(fact);
String factId = (String) record.get("fact_id");
boolean ok = client.verify(factId, System.getenv("MEMVRA_SECRET_KEY"));
```

## Modules
- Root module: Spring Boot API service
- `memvra-client-java`: client SDK for recording and verifying facts

## Tests
- Run unit and integration tests:
```bash
gradle test
```
Integration test uses TestContainers (Docker required) to validate HMAC end-to-end.

## Docs & Roadmap
- Roadmap: `roadmap.md`
- Project Log Book: `logbook.md`

## Production Notes
- Configure DB via environment variables
- Do not use the dev default secret key in production
- Plan improvements: authentication, rate limiting, metrics, structured logging, freshness metadata
