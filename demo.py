import uuid

from knowledge_base import HashEmbeddingService, InMemoryKnowledgeBaseClient
from orchestrator import AgentOrchestrator
from langgraph.orchestrator import build_agnostic_helpdesk


class _MockDoc:
    def __init__(self, page_content):
        self.page_content = page_content


class MockVectorDBClient:
    def __init__(self, docs):
        self.docs = docs

    def similarity_search(self, query, filter=None, k=3):
        # naive: return all docs that match tenant_id in metadata or all
        return [d for d in self.docs][:k]


class MockLLM:
    def invoke(self, prompt):
        # simplistic heuristic: escalate if string ESCALATE present
        if "ESCALATE" in prompt:
            return "ESCALATE"
        return "Scaffolded LLM Response based on local data."


def main():
    tenant_id = "tenant-demo"
    embedder = HashEmbeddingService()
    kb_client = InMemoryKnowledgeBaseClient(embedder)

    kb_client.add_document(
        tenant_id,
        "Our return policy allows customers to return non-damaged goods within 30 days for a full refund.",
        metadata={"source": "Retail Policy", "topic": "returns"},
    )
    kb_client.add_document(
        tenant_id,
        "Our support team can escalate urgent requests to a human advisor if the customer message contains anger or safety concerns.",
        metadata={"source": "Escalation Policy", "topic": "escalation"},
    )

    orchestrator = AgentOrchestrator(
        tenant_id=tenant_id,
        tenant_config={
            "brand_voice": "Professional, empathetic, and customer-centric.",
            "escalation_rules": {"require_human_for": "angry_sentiment"},
            "custom_instructions": "Keep responses short and grounded in the tenant's documented policies.",
        },
        knowledge_base_client=kb_client,
    )

    message = {
        "id": str(uuid.uuid4()),
        "tenant_id": tenant_id,
        "customer_id": "CUST-1001",
        "customer_name": "Ava",
        "content": "What is your return policy and how quickly can I get my refund?",
    }

    result = orchestrator.process_message(message)
    print("=== Demo Result ===")
    print(result)

    # --- Langraph orchestrator smoke run ---
    print('\n=== Langraph Orchestrator Smoke Run ===')
    graph = build_agnostic_helpdesk()
    state = {
        "tenant_id": tenant_id,
        "brand_voice": orchestrator.tenant_config.get("brand_voice"),
        "escalation_rules": orchestrator.tenant_config.get("escalation_rules"),
        "user_message": message["content"],
        "retrieved_context": "",
        "classification": "",
        "conversation_history": [],
    }

    mock_docs = [
        _MockDoc("Our return policy allows refunds within 30 days."),
        _MockDoc("Custom cuts are non-refundable."),
    ]
    vdb = MockVectorDBClient(mock_docs)
    llm = MockLLM()

    out = graph.run(state, vdb, llm)
    print("Langraph run output:")
    print(out)


if __name__ == "__main__":
    main()
