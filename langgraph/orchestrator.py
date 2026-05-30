from typing import TypedDict, List, Annotated
import operator

from langgraph.graph import StateGraph, END

# 1. Define the Agnostic State
class HelpdeskState(TypedDict):
    tenant_id: str
    brand_voice: str
    escalation_rules: dict
    user_message: str
    retrieved_context: str
    classification: str
    conversation_history: Annotated[List[str], operator.add]


def agnostic_intake_node(state: HelpdeskState, *args, **kwargs):
    """
    Frontline agent: retrieves tenant-specific context and categorizes intent.
    """
    print(f"\n--- [Node: Intake] Triggered for Tenant: {state['tenant_id']} ---")

    # Scaffold for multi-tenant vector query
    # results = vector_db.search(query=state['user_message'], filter={"tenant_id": state['tenant_id']})
    # context_str = "\n".join([res.payload for res in results])
    context_str = "Simulated retrieval: Custom cut piping is strictly non-refundable."

    # Scaffold for local LLM inference
    system_prompt = f"""
    Brand Voice: {state['brand_voice']}
    Context: {context_str}
    Rules: {state['escalation_rules']}
    """

    if "angry" in state['user_message'].lower() or "refund" in state['user_message'].lower():
        next_step = "escalation"
        response_text = "I understand you need a refund. Let me get a human manager."
    else:
        next_step = "fulfilment"
        response_text = "Let me check the status of your order based on our policies."

    return {
        "retrieved_context": context_str,
        "classification": next_step,
        "conversation_history": [f"AI: {response_text}"]
    }


def fulfilment_node(state: HelpdeskState, *args, **kwargs):
    """Handles standard operational tasks (e.g., checking order DBs)."""
    print(f"--- [Node: Fulfilment] Executing for Tenant: {state['tenant_id']} ---")
    return {"conversation_history": ["AI: Fulfilment task complete."]}


def escalation_node(state: HelpdeskState, *args, **kwargs):
    """Pushes complex or rule-breaking queries to a human queue."""
    print(f"--- [Node: Escalation] Alerting Human for Tenant: {state['tenant_id']} ---")
    return {"conversation_history": ["System: Ticket escalated to human support."]}


# 3. Building the Directed Graph

def build_agnostic_helpdesk():
    """Compiles the LangGraph state machine."""
    workflow = StateGraph(HelpdeskState)

    workflow.add_node("intake", agnostic_intake_node)
    workflow.add_node("fulfilment", fulfilment_node)
    workflow.add_node("escalation", escalation_node)

    workflow.set_entry_point("intake")
    workflow.add_conditional_edges(
        "intake",
        lambda state: state["classification"],
        {
            "fulfilment": "fulfilment",
            "escalation": "escalation",
        },
    )

    workflow.add_edge("fulfilment", END)
    workflow.add_edge("escalation", END)

    return workflow.compile()
