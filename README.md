# Weaver Agents

**Architect:** Wayne Roberts, Coastal Alpine Tech

**Welcome to Weaver Agents**—a white-label, multi-tenant AI helpdesk scaffold. This repository houses the core engine for tenant-aware routing, isolated knowledge retrieval, and modular local orchestration designed to keep operational data secure and independent.

## The 5 Ws: Project Context

* **Who:** Built by Coastal Alpine Tech Limited, designed for high-stakes Kiwi industries (civil construction, agritech, etc.).
* **What:** A decentralized `langgraph` orchestration layer that safely directs multi-agent tasks and handles local document vectorization.
* **Where:** Engineered at HQ in New Plymouth, Taranaki. Deployable strictly at the edge.
* **When:** Active development. Building robust, compliant localized intelligence.
* **Why:** To guarantee data sovereignty. We are ensuring that tenant operational data never leaks into the cloud by keeping the brains of the operation local and strictly partitioned.

## The Problems We Are Solving

1. **Data Leakage & Compliance:** Sending sensitive industrial data to external LLM providers is a non-starter. We execute entirely locally.
2. **Tenant Cross-Contamination:** Managing multiple clients usually risks data mixing. Our SQLAlchemy ORM models and local vector stores enforce strict, impenetrable tenant isolation.
3. **Rigid Routing:** Static helpdesks can't adapt. Weaver Agents uses a dynamic state graph to intelligently route tasks between specialized local agents.

## System Architecture

```text
┌─────────────────────────────────────────────────────┐
│                   User Request                      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
               ┌─────────────────┐
               │  Orchestrator   │
               │  (langgraph)    │
               └────────┬────────┘
                        │
         ┌──────────────┼──────────────┐
         ▼              ▼              ▼
  ┌────────────┐ ┌────────────┐ ┌────────────┐
  │ Intake     │ │ Fulfilment │ │ Resolution │
  │ Agent      │ │ Agent      │ │ Agent      │
  └──────┬─────┘ └──────┬─────┘ └──────┬─────┘
         │              │              │
         └──────────────┼──────────────┘
                        ▼
         ┌──────────────────────────────┐
         │     Tenant Knowledge Base    │
         │   (Isolated Vector Store)    │
         └──────────────────────────────┘
```
