import pytest
import sys
import os
# Ensure repo-local langgraph package is importable during tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langgraph.orchestrator import build_agnostic_helpdesk


class MockLLM:
    def __init__(self, response: str):
        self.response = response

    def invoke(self, prompt: str) -> str:
        return self.response


class _MockDoc:
    def __init__(self, page_content):
        self.page_content = page_content


class MockVectorDBClient:
    def __init__(self, docs):
        self.docs = docs

    def similarity_search(self, query, filter=None, k=3):
        return [d for d in self.docs][:k]


def test_graph_routes_to_fulfilment():
    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": "t1",
        "brand_voice": "bv",
        "escalation_rules": {},
        "user_message": "normal question",
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }
    docs = [_MockDoc("policy text")]
    vdb = MockVectorDBClient(docs)
    llm = MockLLM("OKAY")
    out = graph.run(state, vdb, llm)
    assert any("Fulfilment task complete" in s for s in out.get("conversation_history", []))


def test_graph_routes_to_escalation():
    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": "t1",
        "brand_voice": "bv",
        "escalation_rules": {},
        "user_message": "this is angry",
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }
    docs = [_MockDoc("policy text")]
    vdb = MockVectorDBClient(docs)
    llm = MockLLM("ESCALATE")
    out = graph.run(state, vdb, llm)
    assert any("Ticket escalated to human support" in s for s in out.get("conversation_history", []))
