"""
Module 5: Multi-Agent Patterns
================================
Build a multi-agent system with a triage agent routing to specialists.

This demonstrates:
- Agents-as-Tools pattern (hierarchical delegation)
- Triage/Router agent that classifies intent
- Specialist agents (Billing, Technical, Returns)
- How agents can call other agents as tools

Usage:
    python module_04_multi_agent/triage_agent.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from shared.data import ORDERS, PRODUCTS, FAQ, TICKETS, next_ticket_id

# ──────────────────────────────────────────────
# Specialist Agent: Billing
# ──────────────────────────────────────────────


@tool
def billing_lookup_order(order_id: str) -> dict:
    """Look up order details for billing inquiries.

    Args:
        order_id: The order ID (e.g., ORD-10001).
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        order = ORDERS[order_id]
        return {
            "order_id": order_id,
            "total": order["total"],
            "items": order["items"],
            "status": order["status"],
            "order_date": order["order_date"],
        }
    return {"error": f"Order {order_id} not found"}


billing_agent = Agent(
    system_prompt="""You are a Billing Specialist at TechStore. You handle:
- Order total inquiries and payment questions
- Invoice requests and receipt generation
- Payment method questions
- Pricing and discount inquiries
- Refund status for returned items

Use the billing_lookup_order tool to find order details.
Always be precise with financial amounts. If you cannot resolve an issue,
recommend the customer contact billing@techstore.example.com.""",
    tools=[billing_lookup_order],
)

# ──────────────────────────────────────────────
# Specialist Agent: Technical Support
# ──────────────────────────────────────────────


@tool
def tech_search_products(query: str) -> list[dict]:
    """Search products for technical specifications.

    Args:
        query: Product name or feature to search for.
    """
    query_lower = query.lower()
    results = []
    for sku, product in PRODUCTS.items():
        if query_lower in product["name"].lower() or query_lower in product["description"].lower():
            results.append({"sku": sku, **product})
    return results if results else [{"message": "No products found"}]


@tool
def tech_search_faq(question: str) -> list[dict]:
    """Search FAQ for technical answers.

    Args:
        question: Technical question to search for.
    """
    question_lower = question.lower()
    results = []
    for faq_entry in FAQ:
        if any(word in faq_entry["question"].lower() or word in faq_entry["answer"].lower()
               for word in question_lower.split() if len(word) > 3):
            results.append(faq_entry)
    return results[:3] if results else []


technical_agent = Agent(
    system_prompt="""You are a Technical Support Specialist at TechStore. You handle:
- Product compatibility questions
- Setup and configuration help
- Troubleshooting product issues
- Product feature and specification inquiries
- Warranty claims for defective products

Use tech_search_products to find product details and tech_search_faq for common solutions.
If the issue requires hands-on support, recommend creating a support ticket.""",
    tools=[tech_search_products, tech_search_faq],
)

# ──────────────────────────────────────────────
# Specialist Agent: Returns & Shipping
# ──────────────────────────────────────────────


@tool
def returns_lookup_order(order_id: str) -> dict:
    """Look up order for return/shipping inquiries.

    Args:
        order_id: The order ID (e.g., ORD-10001).
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        order = ORDERS[order_id]
        return {
            "order_id": order_id,
            "status": order["status"],
            "tracking_number": order.get("tracking_number"),
            "delivery_date": order.get("delivery_date"),
            "return_reason": order.get("return_reason"),
            "items": [item["name"] for item in order["items"]],
        }
    return {"error": f"Order {order_id} not found"}


@tool
def initiate_return(order_id: str, reason: str) -> dict:
    """Initiate a return request for an order.

    Args:
        order_id: The order ID to return.
        reason: Reason for the return.
    """
    order_id = order_id.upper().strip()
    if order_id not in ORDERS:
        return {"error": f"Order {order_id} not found"}

    order = ORDERS[order_id]
    if order["status"] not in ("delivered", "shipped"):
        return {"error": f"Cannot return order with status '{order['status']}'"}

    ticket_id = next_ticket_id()
    ticket = {
        "ticket_id": ticket_id,
        "type": "return",
        "order_id": order_id,
        "reason": reason,
        "status": "return_initiated",
    }
    TICKETS.append(ticket)
    return {"success": True, "ticket_id": ticket_id, "message": "Return initiated. You'll receive a return label via email."}


returns_agent = Agent(
    system_prompt="""You are a Returns & Shipping Specialist at TechStore. You handle:
- Return requests and return policy questions
- Shipping status and tracking inquiries
- Delivery issues (late, damaged, wrong item)
- Exchange requests
- Refund processing timelines

Policies:
- 30-day return window for unused items
- 90-day return for defective items
- Refunds processed in 5-7 business days

Use returns_lookup_order to check order details and initiate_return to start returns.
Always verify the order status before initiating a return.""",
    tools=[returns_lookup_order, initiate_return],
)

# ──────────────────────────────────────────────
# Triage Agent - Routes to Specialists
# ──────────────────────────────────────────────
# This is the "Agents-as-Tools" pattern: specialist agents
# are wrapped as tools that the triage agent can call.


@tool
def route_to_billing(query: str) -> str:
    """Route the customer's query to the Billing Specialist agent.
    Use this for questions about payments, invoices, order totals, pricing, or refund amounts.

    Args:
        query: The customer's billing-related question.
    """
    response = billing_agent(query)
    return response.message.content[0]["text"] if response.message.content else str(response)


@tool
def route_to_technical(query: str) -> str:
    """Route the customer's query to the Technical Support agent.
    Use this for questions about product features, setup, troubleshooting, or compatibility.

    Args:
        query: The customer's technical question.
    """
    response = technical_agent(query)
    return response.message.content[0]["text"] if response.message.content else str(response)


@tool
def route_to_returns(query: str) -> str:
    """Route the customer's query to the Returns & Shipping agent.
    Use this for return requests, shipping status, tracking, delivery issues, or exchanges.

    Args:
        query: The customer's returns or shipping question.
    """
    response = returns_agent(query)
    return response.message.content[0]["text"] if response.message.content else str(response)


# The triage agent decides which specialist to route to
triage_agent = Agent(
    system_prompt="""You are the Triage Agent for TechStore customer support.

Your ONLY job is to:
1. Greet the customer warmly
2. Understand their issue
3. Route them to the right specialist agent

Available specialists:
- route_to_billing: For payment, pricing, invoice, order total, and refund amount questions
- route_to_technical: For product features, setup, troubleshooting, and compatibility questions
- route_to_returns: For returns, shipping, tracking, delivery issues, and exchanges

Rules:
- Always route to a specialist - don't try to answer yourself
- If unclear, ask one clarifying question before routing
- Pass the customer's full question/context to the specialist
- Present the specialist's response to the customer naturally
- If the issue spans multiple areas, handle one at a time""",
    tools=[route_to_billing, route_to_technical, route_to_returns],
)


def main():
    print("=" * 60)
    print("  SupportBot Multi-Agent System")
    print("  Triage Agent -> Specialist Agents")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()
    print("  Try: 'How much did I pay for order ORD-10001?'  (-> Billing)")
    print("  Try: 'I want to return order ORD-10004'          (-> Returns)")
    print("  Try: 'Does the webcam work with Linux?'          (-> Technical)")
    print()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nSupportBot: Thanks for chatting! Have a great day!")
            break
        if not user_input:
            continue

        print("\nSupportBot: ", end="", flush=True)
        response = triage_agent(user_input)
        print()
        print()


if __name__ == "__main__":
    main()
