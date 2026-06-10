import uuid
from typing import Any, Dict, Optional

from agents import FulfilmentAgent, IntakeAgent, ResolutionAgent
from knowledge_base import HashEmbeddingService, InMemoryKnowledgeBaseClient, KnowledgeBaseClient


class InMemoryMemoryStore:
    """Simple memory store for conversation state in demos and unit tests."""

    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def update_context(self,
                       interaction_id: str,
                       customer_profile: Dict[str,
                                              Any],
                       classification: str) -> None:
        self.store[interaction_id] = {
            "customer_profile": customer_profile,
            "classification": classification,
        }


class NoOpCRM:
    def update_customer(self, *args, **kwargs):
        return {}


class NoOpLLMPool:
    def generate(self, prompt: str) -> str:
        return f"[LLM response generated from prompt: {prompt[:120]}...]"


class NoOpTelemetryLogger:
    def log_event(self, event_name: str, data: Dict[str, Any]) -> None:
        print(f"Telemetry: {event_name}", data)


class NoOpEscalationQueue:
    def push(self, context: Dict[str, Any]) -> None:
        print(f"Escalation queue received context: {context}")


class AgentOrchestrator:
    """High-level orchestrator for tenant-aware agent routing."""

    def __init__(
        self,
        tenant_id: str,
        tenant_config: Optional[Dict[str, Any]] = None,
        knowledge_base_client: Optional[KnowledgeBaseClient] = None,
        memory_store: Optional[InMemoryMemoryStore] = None,
    ):
        self.tenant_id = tenant_id
        self.tenant_config = tenant_config or {}
        self.memory_store = memory_store or InMemoryMemoryStore()
        self.kb_client = knowledge_base_client or InMemoryKnowledgeBaseClient(
            HashEmbeddingService())
        self.crm_client = NoOpCRM()
        self.llm_pool = NoOpLLMPool()
        self.telemetry_logger = NoOpTelemetryLogger()
        self.escalation_queue = NoOpEscalationQueue()

    def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        intake_agent = IntakeAgent(
            knowledge_base_client=self.kb_client,
            memory_store=self.memory_store,
            tenant_id=self.tenant_id,
            tenant_config=self.tenant_config,
        )

        result = intake_agent.process_interaction(message)
        if result.get("status") == "handoff_required":
            return self._route_handoff(result)

        return result

    def _route_handoff(self, handoff: Dict[str, Any]) -> Dict[str, Any]:
        target = handoff.get("target_agent")
        context = handoff.get("context", {})

        if target == "FulfillmentAgent":
            agent = FulfilmentAgent(
                crm_client=self.crm_client,
                order_db=None,
                llm_pool=self.llm_pool,
                tenant_id=self.tenant_id,
                escalation_rules=self.tenant_config.get(
                    "escalation_rules",
                    {}),
            )
            return agent.execute_task({"intent": "process_order", **context})

        if target == "ResolutionAgent":
            agent = ResolutionAgent(
                telemetry_logger=self.telemetry_logger,
                escalation_queue=self.escalation_queue,
                tenant_id=self.tenant_id,
            )
            return agent.handle_issue(
                {"issue_id": str(uuid.uuid4()), **context})

        return {"status": "unknown_target", "target_agent": target}


def build_sample_orchestrator() -> AgentOrchestrator:
    kb_client = InMemoryKnowledgeBaseClient(HashEmbeddingService())
    return AgentOrchestrator(
        tenant_id="tenant-demo",
        tenant_config={
            "brand_voice": "Friendly, concise and professional.",
            "escalation_rules": {
                "require_human_for": "high_risk"},
            "custom_instructions": "Always cite the tenant knowledge base and avoid speculation.",
        },
        knowledge_base_client=kb_client,
    )
