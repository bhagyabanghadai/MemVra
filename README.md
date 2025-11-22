# MemVra Truth Ledger

MemVra is a cryptographically verifiable "Truth Ledger" for AI Agents. It allows agents to record facts with mandatory provenance, which are then signed with HMAC-SHA256 and stored in an immutable ledger.

## 🚀 Features

### Core "Truth Oracle"
- **Immutable Ledger**: Facts are cryptographically signed upon recording.
- **Integrity Verification**: Every read operation re-computes the hash to ensure data hasn't been tampered with.
- **Time-Travel Search**: Query facts as they existed at any point in time.
- **Fact Revocation**: Explicitly revoke incorrect facts with a reason, maintaining the audit trail.

### Developer Experience
- **Developer Dashboard**: Manage API keys and view usage statistics.
- **Granular API Keys**: Generate unique keys for different agents.
- **Full-Stack Pagination**: Efficiently browse millions of records.
- **Advanced Search**: Filter by Source ID, Source Type, Agent ID, and Date Range.

## 🛠 Tech Stack

### Backend
- **Java 17** & **Spring Boot 3.2**
- **PostgreSQL** (Data Storage)
- **Flyway** (Database Migrations)
- **Spring Security + JWT** (Authentication)

### Frontend
- **React** & **TypeScript**
- **TailwindCSS** (Styling)
- **TanStack Query** (State Management)
- **Framer Motion** (Animations)

## 🏁 Getting Started

### Prerequisites
- Java 17+
- Node.js 18+
- Docker & Docker Compose

### Quick Start (Full Stack)

1. **Start Infrastructure (DB & Backend)**
   ```bash
   docker compose up -d
   ```
   The backend will be available at `http://localhost:8080`.

2. **Start Frontend**
   ```bash
   cd memvra-frontend
   npm install
   npm run dev
   ```
   Open `http://localhost:5173` in your browser.

3. **Create an Account**
   - Go to `http://localhost:5173/signup`.
   - Create an account and log in.
   - Navigate to the **Dashboard** to generate your first API Key.

## 📖 API Documentation

### Authentication
Include your API Key in the header of requests:
`X-API-Key: mv_sk_...`

### Endpoints

#### Record a Fact
```http
POST /v1/facts
Content-Type: application/json

{
  "content": "User prefers dark mode",
  "source_type": "user_input",
  "source_id": "chat:123",
  "recorded_by": "agent-007"
}
```

#### Search Facts
```http
GET /v1/facts?source_id=chat:123&from_date=2023-01-01T00:00:00Z
```

#### Get Fact with Verification
```http
GET /v1/facts/{fact_id}
```
*Returns 200 OK only if the cryptographic signature is valid.*

#### Revoke a Fact
```http
POST /v1/facts/{fact_id}/revoke
Content-Type: application/json

{
  "reason": "User corrected their statement"
}
```

## 🔒 Security

- **HMAC-SHA256**: All facts are signed using a secret key stored on the server.
- **JWT**: User sessions for the dashboard are managed via stateless JWTs.
- **Database-Backed Keys**: API keys are hashed (SHA-256) before storage.

## 📂 Project Structure

- `src/main/java`: Spring Boot Backend
- `memvra-frontend`: React Frontend
- `deployment`: Kubernetes/Cloud Run configs
- `scripts`: Verification and utility scripts

## 🧪 Testing

Run the full verification suite:
```bash
python scripts/verify_deployment.py
```

## 📜 License

MIT
