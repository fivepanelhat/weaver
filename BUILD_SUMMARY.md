# Coastal Alpine Tech Agentic Helpdesk Build Summary

## Overview
This repository defines a white-label, multi-tenant AI helpdesk platform with a governance and architecture focus.

Key components:
- `agents.py` — agent scaffolding for Intake, Fulfillment, and Resolution, with tenant-aware runtime fields and RAG prompt assembly.
- `models.py` — SQLAlchemy ORM models for tenants, tenant configs, knowledge sources, vector embeddings, and interaction logs.
- `database.py` — tenant-aware database initialization and helper functions for secure tenant-scoped queries.
- `knowledge_base.py` — tenant-isolated embedding and knowledge retrieval abstractions for demo and SQLAlchemy-backed stores.
- `orchestrator.py` — high-level tenant-aware orchestrator that routes messages through Intake, Fulfillment, and Resolution agents.
 - `orchestrator.py` — high-level tenant-aware orchestrator that routes messages through Intake, Fulfillment, and Resolution agents. Now integrated with `langgraph` for a modular state-graph based flow and smoke-test harness.
- `demo.py` — runnable demo script for conversation flow using in-memory tenant knowledge and RAG prompt generation.
- `agent_knowledge_base/` — governance documentation covering corporate policy, ethics, community DAO governance, platform runbook, and database schema.

## Architecture Summary
The platform is designed for multi-tenant deployment with strict tenant isolation in both relational and semantic layers.

### Relational Core (PostgreSQL)
- `tenants` stores business accounts and subscription metadata.
- `tenant_configs` stores tenant-specific runtime settings such as brand voice, escalation rules, and active channels.
- `knowledge_sources` catalogs uploaded or linked documents for each tenant.
- `interaction_logs` records every customer interaction with tenant context, escalation status, and audit metadata.

### Semantic Memory / Vector Store
- Uses a separate vector layer for RAG embeddings.
- Supports MILVUS or PostgreSQL `pgvector`.
- Every embedding and search query is tenant-partitioned by `tenant_id`.
- Retrieval is designed to enforce tenant isolation before similarity ranking.

### Agent Flow
1. Request enters through the Intake Agent.
2. Tenant context is resolved and tenant-specific config is loaded.
3. The query is searched against tenant-scoped embeddings.
4. Results are assembled into an LLM prompt with tenant brand and escalation rules.
5. The LLM response is generated and recorded against tenant-specific logs.
6. Handoffs or escalations are routed through Fulfillment and Resolution agents.

## Governance and Documentation
A governance knowledge base exists in `agent_knowledge_base/`:
- `corporate_frameworks.md` — high-level policy and framework summary
- `ethics_review_playbook.md` — ethics review workflow and decision criteria
- `dao_charter.md` — Digital Taonga DAO governance and community consent rules
- `platform_runbook.md` — operational runbook for change control, incident response, and agent deployment
- `Context/multi_tenant_database_schema.md` — multi-tenant database and vector store design
- `governance_index.md` — single-page index for the governance knowledge base
- `README.md` — guidance for using the knowledge base

## Build Status
- ORM models and schema design are defined in `models.py`.
- Tenant-aware DB initialization exists in `database.py`.
- `agents.py` includes tenant-aware scaffolding, with generic task handling, handoff logic, and RAG prompt assembly.
- `knowledge_base.py` provides tenant-isolated embedding and retrieval abstractions.
- `orchestrator.py` implements a tenant-aware routing layer and is now integrated with the repo-local `langgraph/` state-graph package.
- `langgraph/` contains the active local package for graph orchestration, LLM wrappers, and embedding helpers; duplicate external copies have been removed.
- `demo.py` validates the workflow with an in-memory knowledge base and prompt generation; the demo run has been verified.
- Governance docs have been harmonized with consistent headings, review cycles, and NZ legal references.

## Dependencies
- See `requirements.txt` for required Python packages.
- Install with:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## How to run
1. Activate the repository virtual environment:

```powershell
cd "c:\Users\Admin\Gemini Agents"
.venv\Scripts\Activate.ps1
```

2. Run the demo script:

```powershell
.venv\Scripts\python.exe demo.py
```

3. To validate imports and database setup, run:

```powershell
.venv\Scripts\python.exe -c "import models, database; print('imports ok')"
```

4. If you want to initialize a live PostgreSQL instance, set `DATABASE_URL` and run the import test again.

```powershell
$env:DATABASE_URL = 'postgresql://<user>:<password>@<host>:<port>/<dbname>'
.venv\Scripts\python.exe -c "import models, database; print('postgres init ok')"
```

5. To create the database schema manually, use a PostgreSQL client or `psql`:

```powershell
psql "postgresql://<user>:<password>@<host>:<port>/<dbname>" -c "CREATE EXTENSION IF NOT EXISTS pgvector;"
```

> Note: `database.py` will attempt to initialize PostgreSQL tables on import using `DATABASE_URL` or the default `postgresql://user:password@localhost/coastal_alpine_helpdesk`.

## Next Steps
- Integrate `SqlAlchemyKnowledgeBaseClient` from `knowledge_base.py` into the orchestrator for DB-backed RAG retrieval.
- Add real embedding support (OpenAI, local LLM, or pgvector/Milvus) and move beyond the demo hash embedder.
 - Wire local sovereign embedding engine: `langgraph/embeddings.py` now provides `SovereignEmbeddingEngine` with Ollama support and deterministic fallback; `knowledge_base.SqlAlchemyKnowledgeBaseClient` will use `embed_and_store` when available to persist vectors via `TenantAwareDB.add_vector_embedding`.
 - Add local LLM wrapper: `langgraph/llm.py` exposes `LocalSovereignLLM` which uses Ollama when available, with a deterministic fallback for offline smoke tests. `langgraph.orchestrator` now invokes pluggable LLMs.
 - Add state-graph orchestration: `langgraph/graph.py` implements a lightweight `StateGraph` runner; `langgraph/orchestrator.py` contains intake, fulfilment, and escalation nodes.
 - Tests: Added `tests/test_orchestrator.py` for node routing; run with `pytest`.
- Add migration support (Alembic) for PostgreSQL schema evolution.
- Wire interaction logging and escalation flows into a production-ready orchestration layer.
- Replace placeholder governance links with internal wiki or canonical URLs.
- Export the knowledge base into a single review-ready package if needed.
