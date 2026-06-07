# Weaver Agents Changelog

All notable changes to the `weaver` repository will be documented in this file.

## [1.0.0] - 2026-06-07

### Added
- Integrated local `langgraph` state engine package.
- Scaffolding for multi-tenant database using SQLAlchemy models (`models.py`, `database.py`).
- Tenant-scoped retrieval interface in `knowledge_base.py`.
- Demonstration agent flow `demo.py`.
- Governance docs in `agent_knowledge_base/`.
- Standardized README, `.env.example`, `CHANGELOG.md`, `CONTRIBUTING.md`, and `requirements-dev.txt`.
- Added test suite validation under `tests/test_orchestrator.py`.
