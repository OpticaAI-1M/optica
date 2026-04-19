

<p align="center">
  <img src="./assets/images/logo.png" alt="Optica Logo" width="600" />
</p>


### AI-Powered Production Incident Intelligence Platform

**Operational clarity, powered by AI**

See every incident down to the root cause.

<p>
  <a href="#quick-start"><img src="https://img.shields.io/badge/Get%20Started-5%20Minutes-185FA5?style=for-the-badge" /></a>
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/PostgreSQL-pgvector-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
</p>

<p>
  <img src="https://img.shields.io/badge/License-MIT-0C447C?style=flat-square" />
  <img src="https://img.shields.io/badge/Status-Active%20Development-185FA5?style=flat-square" />
  <img src="https://img.shields.io/badge/AI-RAG%20%2B%20Tools-378ADD?style=flat-square" />
  <img src="https://img.shields.io/badge/Auth-Keycloak-0C447C?style=flat-square" />
</p>
</div>

---

<p align="center">
  <img src="./assets/images/hero-banner.png" alt="Optica Hero Banner" width="100%" />
</p>

## Why Optica?

Production incidents are noisy, fragmented, and expensive.

When a critical issue occurs, engineers usually spend 30–90 minutes jumping across:

* Slack threads
* Jira tickets
* Logs and dashboards
* Deployment history
* Runbooks and tribal knowledge

By the time the root cause is identified, MTTR is already high.

Optica changes that.

Optica is an AI-powered incident intelligence platform built for engineering and SRE teams. It combines historical incidents, deployment changes, uploaded logs, runbooks, and live system context into a single AI-generated investigation flow.

Instead of manually searching across multiple tools, an engineer can create an incident, upload evidence, and receive:

* Similar historical incidents
* AI-generated root cause analysis
* Confidence score
* Recommended remediation steps
* Relevant deployment changes and evidence

—all in under 60 seconds.

> No hallucinated answers. Every recommendation is backed by your own incidents, documents, and runbooks.

---

## Key Capabilities

<table>
<tr>
<td width="33%">

### Incident Intelligence

Create incidents, upload logs, and track every action in one place.

</td>
<td width="33%">

### Retrieval-Augmented RCA

Uses hybrid retrieval (BM25 + semantic search) across previous incidents and runbooks.

</td>
<td width="33%">

### Tool-Driven Investigation

Calls live system tools such as deployment history, release changes, and external APIs.

</td>
</tr>
<tr>
<td>

### Audit & Governance

Every AI action, recommendation, and user activity is stored in an immutable audit trail.

</td>
<td>

### Role-Based Access Control

Enterprise-ready authentication and RBAC powered by Keycloak.

</td>
<td>

### Local LLM Support

Run entirely on your infrastructure using Ollama + Llama3.

</td>
</tr>
</table>

---

## How It Works

<p align="center">
  <img src="./assets/images/incident-flow.png" alt="Optica Incident Flow" width="95%" />
</p>

1. Engineer authenticates via Keycloak
2. A new incident is created in Optica
3. Logs, documents, or screenshots are uploaded
4. Celery workers process files asynchronously
5. Documents are chunked and embedded into pgvector
6. Hybrid search retrieves similar incidents and runbooks
7. MCP tools fetch deployment changes and live context
8. The LLM synthesizes evidence and generates:

   * Root cause
   * Confidence score
   * Recommended next steps
9. Every action is written to the audit log

---

## Architecture

<p align="center">
  <img src="./assets/images/architecture.png" alt="Optica Architecture" width="100%" />
</p>

| Layer             | Technology              | Purpose                                   |
| ----------------- | ----------------------- | ----------------------------------------- |
| Frontend          | React + Tailwind        | Incident dashboard and investigation UI   |
| API Layer         | FastAPI                 | Backend APIs and orchestration            |
| Authentication    | Keycloak                | JWT auth and RBAC                         |
| Database          | PostgreSQL + pgvector   | Structured data + vector embeddings       |
| Queue             | RabbitMQ + Celery       | Async ingestion and background processing |
| AI Pipeline       | LangChain + Ollama      | RAG workflow and local inference          |
| Tool Integrations | MCP / GitHub APIs       | Deployment and release intelligence       |
| Audit Layer       | PostgreSQL audit tables | Traceability and governance               |

### System Ports

| Component  | Port         |
| ---------- | ------------ |
| Frontend   | 3000         |
| API        | 8000         |
| Keycloak   | 8080         |
| PostgreSQL | 5432         |
| RabbitMQ   | 5672 / 15672 |
| Ollama     | 11434        |

---

## Tech Stack

| Stack                 | Version        | Purpose                     |
| --------------------- | -------------- | --------------------------- |
| Python / FastAPI      | 3.11+ / 0.110+ | Backend API server          |
| PostgreSQL + pgvector | 15+ / 0.5+     | Database and vector storage |
| Keycloak              | 23+            | Authentication and RBAC     |
| RabbitMQ + Celery     | 3.12+ / 5.3+   | Background processing       |
| LangChain + Ollama    | 0.1+ / Latest  | RAG pipeline and local LLM  |
| React + Tailwind      | 18+ / 3+       | Frontend UI                 |
| Docker Compose        | 2.20+          | Local orchestration         |

---

# Quick Start

## Prerequisites

* Docker Desktop 4.20+
* Docker Compose 2.20+
* Git
* Minimum 8 GB RAM
* Ollama installed locally

```bash
git clone https://github.com/your-org/optica.git
cd optica
```

### Configure Environment

```bash
cp .env.example .env
```

### Pull the Local LLM

```bash
ollama pull llama3
```

### Start All Services

```bash
docker compose up -d
```

### Run Database Migrations

```bash
docker compose exec api alembic upgrade head
```

### Import Keycloak Realm

```bash
docker compose exec keycloak /opt/keycloak/bin/kc.sh import \
  --file /opt/keycloak/data/import/optica-realm.json
```

### Open the Platform

| Service            | URL                                                      |
| ------------------ | -------------------------------------------------------- |
| Frontend           | [http://localhost:3000](http://localhost:3000)           |
| API Docs           | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Keycloak           | [http://localhost:8080](http://localhost:8080)           |
| RabbitMQ Dashboard | [http://localhost:15672](http://localhost:15672)         |

---

## Environment Variables

| Variable          | Default                                     | Description               |
| ----------------- | ------------------------------------------- | ------------------------- |
| `DATABASE_URL`    | `postgresql://optica:optica@db:5432/optica` | PostgreSQL connection     |
| `KEYCLOAK_URL`    | `http://keycloak:8080`                      | Keycloak server           |
| `KEYCLOAK_REALM`  | `optica`                                    | Realm name                |
| `RABBITMQ_URL`    | `amqp://guest:guest@rabbitmq:5672/`         | RabbitMQ connection       |
| `OLLAMA_URL`      | `http://host.docker.internal:11434`         | Ollama inference endpoint |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2`                          | Embedding model           |
| `GITHUB_TOKEN`    | Optional                                    | Deployment lookup access  |

---

## Repository Structure

```text
optica/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── services/
│   │   ├── workers/
│   │   └── ai/
│   ├── alembic/
│   └── tests/
├── frontend/
├── infra/
│   ├── keycloak/
│   └── docker/
├── assets/
│   └── images/
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## API Surface

| Method | Endpoint                          | Access    | Description                   |
| ------ | --------------------------------- | --------- | ----------------------------- |
| POST   | `/auth/login`                     | Public    | Obtain JWT token              |
| GET    | `/incidents`                      | Any Role  | List incidents                |
| POST   | `/incidents`                      | Engineer+ | Create incident               |
| GET    | `/incidents/{id}`                 | Any Role  | Get incident details          |
| PATCH  | `/incidents/{id}/status`          | Manager+  | Update incident status        |
| POST   | `/incidents/{id}/documents`       | Engineer+ | Upload logs/documents         |
| POST   | `/incidents/{id}/analyze`         | Engineer+ | Trigger AI analysis           |
| GET    | `/incidents/{id}/recommendations` | Any Role  | Fetch RCA and recommendations |
| GET    | `/audit-logs`                     | Admin     | View complete audit trail     |

---

## Screenshots


<table>
<tr>
<td>
<img src="./assets/images/screenshot-dashboard.png" alt="Dashboard Screenshot" />
<p align="center"><b>Incident Dashboard</b></p>
</td>
<td>
<img src="./assets/images/screenshot-root-cause.png" alt="Root Cause Screenshot" />
<p align="center"><b>AI Root Cause Analysis</b></p>
</td>
</tr>
</table>

---

## Governance & Trust

Optica is designed for production environments where traceability matters.

* Every AI recommendation is backed by evidence
* Every user action is logged
* Every generated RCA is auditable
* Role-based access ensures least-privilege access
* Supports local models for data privacy and compliance

This makes Optica suitable for:

* Enterprise engineering teams
* Regulated environments
* Internal production support platforms
* High-trust AI operations workflows

---

## Running Tests

```bash
# Run all tests
docker compose exec api pytest

# Run a specific test module
docker compose exec api pytest tests/test_incidents.py -v

# Run with coverage
docker compose exec api pytest --cov=app --cov-report=html
```

---

## Roadmap

* [ ] Slack integration
* [ ] Jira synchronization
* [ ] Kubernetes and Datadog connectors
* [ ] Multi-agent incident investigation
* [ ] Incident timeline visualization
* [ ] Automated remediation suggestions
* [ ] Team knowledge graph
* [ ] Cloud deployment templates

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow the Repository + Service layer architecture
4. Ensure new endpoints include JWT auth
5. Add tests for all new functionality
6. Open a pull request with a clear explanation

```bash
git checkout -b feature/your-feature
```

---

<div align="center">

Built for engineers who need answers, not more tabs.

**Optica — from noise to root cause, in focus.**

</div>

