# Weaver Agents | AI-Native Sovereign Mesh

This repository houses **Gemini Agents**, a white-label, multi-tenant AI helpdesk scaffold engineered by Coastal Alpine Tech Limited. It features tenant-aware routing, isolated knowledge retrieval, and a modular local `langgraph` orchestration layer built to keep operational data secure and independent.

Designed for high-stakes Kiwi industries—from civil construction to agritech—this framework ensures that localized intelligence stays robust, compliant, and right at the edge.

## 🏗️ Repository Architecture
Here is how the engine room is laid out under the hood:

### 1. Root Orchestration Files

- `agents.py` — Agent scaffolding managing the end-to-end lifecycle: intake, fulfilment, and resolution.
- `orchestrator.py` — Core execution layer coordinating multi-agent task distribution.
- `models.py` — SQLAlchemy ORM models enforcing strict tenant isolation, configuration management, and interaction history.
- `database.py` — Tenant-aware database initialization and multi-tenant helper functions.
- `knowledge_base.py` — Tenant-isolated vector embedding and local retrieval engine.
- `demo.py` — Operational sandbox script to test local end-to-end agent runs.
- `BUILD_SUMMARY.md` — Internal build tracking and deployment states.

### 2. Core Modules

- `langgraph/` — The AI-native nervous system of the platform.
  - `graph.py` — State graph definitions and conditional routing logic.
  - `embeddings.py` & `ingestion.py` — Local document vectorization pipelines.
  - `llm.py` — Local model interfaces ensuring data sovereignty.
  - `orchestrator.py` — Graph orchestration and local execution coordination.

- `agent_knowledge_base/` — Governance, risk, and compliance frameworks.
  - `dao_charter.md` & `governance_index.md` — Decentralized sovereignty structures.
  - `ethics_review_playbook.md` & `platform_runbook.md` — Guardrails for autonomous execution.

- `tests/` — Local testing testbeds utilizing `pytest` to guarantee deterministic agent routing.

## Local `langgraph` package

This repository uses the local package at `langgraph/` for graph-based orchestration and local LLM/embedding support. Do not install or use an external `Langraph` package from a different folder.

To import from the repo-local package, use:

```python
from langgraph.orchestrator import build_agnostic_helpdesk
```

## Getting started

1. Activate the virtual environment:

```powershell
cd "c:\Users\Admin\Gemini Agents"
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Run the demo:

```powershell
.venv\Scripts\python.exe demo.py
```

4. Run tests:

```powershell
.venv\Scripts\pytest.exe -q
```
