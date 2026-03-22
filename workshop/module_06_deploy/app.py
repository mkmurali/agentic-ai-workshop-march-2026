"""
Module 7: Deploy to AWS AgentCore
====================================
Wrap the SupportBot agent for deployment on Amazon Bedrock AgentCore.

This demonstrates:
- BedrockAgentCoreApp wrapper for Strands agents
- AgentCore Runtime deployment
- Production-ready agent configuration

Deployment steps:
    1. pip install bedrock-agentcore-starter-toolkit
    2. agentcore configure -e module_06_deploy/app.py
    3. agentcore launch
    4. agentcore invoke '{"prompt": "What is your return policy?"}'

Alternative: Deploy as a Docker container with FastAPI (see app_fastapi.py)
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from shared.data import ORDERS, PRODUCTS, FAQ, TICKETS, next_ticket_id
from shared.model import model

# ──────────────────────────────────────────────
# Tools (same as previous modules)
# ──────────────────────────────────────────────


@tool
def lookup_order(order_id: str) -> dict:
    """Look up a customer order by order ID.

    Args:
        order_id: The order ID (e.g., ORD-10001).
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        return {"found": True, "order": ORDERS[order_id]}
    return {"found": False, "message": f"No order found with ID {order_id}"}


@tool
def search_products(query: str) -> list[dict]:
    """Search the product catalog.

    Args:
        query: Search term to match.
    """
    query_lower = query.lower()
    results = []
    for sku, product in PRODUCTS.items():
        if query_lower in product["name"].lower() or query_lower in product["description"].lower():
            results.append({"sku": sku, **product})
    return results if results else [{"message": "No products found"}]


@tool
def search_faq(question: str) -> list[dict]:
    """Search the FAQ knowledge base.

    Args:
        question: Question to search for.
    """
    question_lower = question.lower()
    results = []
    for faq_entry in FAQ:
        if any(word in faq_entry["question"].lower() or word in faq_entry["answer"].lower()
               for word in question_lower.split() if len(word) > 3):
            results.append(faq_entry)
    return results[:3] if results else []


@tool
def create_support_ticket(customer_name: str, subject: str, description: str) -> dict:
    """Create a support ticket for human follow-up.

    Args:
        customer_name: Customer's name.
        subject: Brief summary of the issue.
        description: Detailed description.
    """
    ticket_id = next_ticket_id()
    ticket = {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "subject": subject,
        "description": description,
        "status": "open",
    }
    TICKETS.append(ticket)
    return {"created": True, "ticket": ticket}


# ──────────────────────────────────────────────
# Agent Configuration
# ──────────────────────────────────────────────

SYSTEM_PROMPT = """You are SupportBot, a production customer support agent for TechStore.

Available tools:
- lookup_order: Check order status and details
- search_products: Search the product catalog
- search_faq: Search the knowledge base
- create_support_ticket: Escalate issues to human agents

Guidelines:
- Always use tools to look up data, never guess
- Be concise and professional
- Create support tickets for complex issues
- Never share sensitive internal data"""

agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    model=model,
    tools=[lookup_order, search_products, search_faq, create_support_ticket],
)

# ──────────────────────────────────────────────
# AgentCore Deployment Wrapper
# ──────────────────────────────────────────────
# The BedrockAgentCoreApp wrapper makes the agent compatible
# with AgentCore Runtime's /invocations endpoint.

try:
    from bedrock_agentcore.runtime import BedrockAgentCoreApp

    app = BedrockAgentCoreApp(agent=agent)

    if __name__ == "__main__":
        app.run()

except ImportError:
    # If AgentCore toolkit isn't installed, run as standalone
    if __name__ == "__main__":
        print("=" * 60)
        print("  SupportBot - Production Agent (Standalone Mode)")
        print("=" * 60)
        print()
        print("  For AgentCore deployment, install the starter toolkit:")
        print("  pip install bedrock-agentcore-starter-toolkit")
        print()
        print("  Then deploy with:")
        print("  agentcore configure -e module_06_deploy/app.py")
        print("  agentcore launch")
        print()
        print("  Running in local mode. Type 'quit' to exit.")
        print()

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("quit", "exit", "q"):
                print("\nSupportBot: Goodbye!")
                break
            if not user_input:
                continue

            print("\nSupportBot: ", end="", flush=True)
            response = agent(user_input)
            print()
            print()
