"""
Module 3A: Custom Tools
========================
Extend the agent with custom tools using the @tool decorator.

This demonstrates:
- Creating tools with @tool decorator
- Type hints and docstrings as tool schemas
- Connecting tools to the agent
- The agentic loop with tool calling (reason → call tool → observe → respond)

Usage:
    python module_02_tools_mcp/tools.py
"""

import sys
import os

# Add parent directory to path for shared imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from shared.data import ORDERS, PRODUCTS, FAQ, TICKETS, next_ticket_id

# ──────────────────────────────────────────────
# Custom Tools - Each @tool function becomes available to the agent
# ──────────────────────────────────────────────


@tool
def lookup_order(order_id: str) -> dict:
    """Look up a customer order by its order ID.

    Args:
        order_id: The order ID to look up (e.g., ORD-10001)

    Returns:
        Order details including status, items, and tracking information.
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        return {"found": True, "order": ORDERS[order_id]}
    return {"found": False, "message": f"No order found with ID {order_id}"}


@tool
def search_products(query: str, category: str = "") -> list[dict]:
    """Search the product catalog by name or category.

    Args:
        query: Search term to match against product names and descriptions.
        category: Optional category filter (Electronics, Furniture, Accessories).

    Returns:
        List of matching products with details and availability.
    """
    query_lower = query.lower()
    results = []
    for sku, product in PRODUCTS.items():
        if category and product["category"].lower() != category.lower():
            continue
        if (query_lower in product["name"].lower()
                or query_lower in product["description"].lower()
                or query_lower in product["category"].lower()):
            results.append({"sku": sku, **product})
    return results if results else [{"message": f"No products found matching '{query}'"}]


@tool
def search_faq(question: str) -> list[dict]:
    """Search the FAQ knowledge base for answers to common questions.

    Args:
        question: The customer's question to search for.

    Returns:
        Relevant FAQ entries with questions and answers.
    """
    question_lower = question.lower()
    results = []
    for faq_entry in FAQ:
        # Simple keyword matching - in production, you'd use embeddings/RAG
        if any(word in faq_entry["question"].lower() or word in faq_entry["answer"].lower()
               for word in question_lower.split() if len(word) > 3):
            results.append(faq_entry)
    return results[:3] if results else [{"message": "No FAQ entries found. Let me try to help you directly."}]


@tool
def create_support_ticket(
    customer_name: str,
    customer_email: str,
    subject: str,
    description: str,
    priority: str = "medium",
) -> dict:
    """Create a new support ticket for issues that need human follow-up.

    Args:
        customer_name: The customer's full name.
        customer_email: The customer's email address.
        subject: Brief summary of the issue.
        description: Detailed description of the problem.
        priority: Ticket priority - low, medium, or high.

    Returns:
        The created ticket with its ID and details.
    """
    ticket_id = next_ticket_id()
    ticket = {
        "ticket_id": ticket_id,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "subject": subject,
        "description": description,
        "priority": priority,
        "status": "open",
    }
    TICKETS.append(ticket)
    return {"created": True, "ticket": ticket}


@tool
def check_product_availability(sku: str) -> dict:
    """Check if a specific product is currently in stock.

    Args:
        sku: The product SKU to check (e.g., SKU-001).

    Returns:
        Stock availability status for the product.
    """
    sku = sku.upper().strip()
    if sku in PRODUCTS:
        product = PRODUCTS[sku]
        return {
            "sku": sku,
            "name": product["name"],
            "in_stock": product["in_stock"],
            "price": product["price"],
        }
    return {"found": False, "message": f"No product found with SKU {sku}"}


# ──────────────────────────────────────────────
# System Prompt - Updated with tool awareness
# ──────────────────────────────────────────────
SYSTEM_PROMPT = """You are SupportBot, a friendly and helpful customer support agent for TechStore,
an online electronics and accessories retailer.

You have access to the following tools:
- lookup_order: Look up order details by order ID
- search_products: Search the product catalog
- search_faq: Search the FAQ knowledge base
- create_support_ticket: Create a ticket for human follow-up
- check_product_availability: Check if a product is in stock

Guidelines:
- Always use tools to look up real data - never make up information
- Search the FAQ first for common questions
- If a customer mentions an order, look it up by order ID
- Create a support ticket if the issue needs human intervention
- Be polite, concise, and accurate"""

# ──────────────────────────────────────────────
# Create Agent with Tools
# ──────────────────────────────────────────────
agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[lookup_order, search_products, search_faq, create_support_ticket, check_product_availability],
)


def main():
    print("=" * 60)
    print("  SupportBot with Tools - AI Customer Support Agent")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()
    print("  Try: 'What's the status of order ORD-10002?'")
    print("  Try: 'Do you have any headphones in stock?'")
    print("  Try: 'What's your return policy?'")
    print()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nSupportBot: Thanks for chatting! Have a great day!")
            break
        if not user_input:
            continue

        # Now the agent loop includes tool calling:
        #   1. Sends user message + system prompt + tool definitions to LLM
        #   2. LLM reasons and decides which tool(s) to call
        #   3. Strands executes the tool and returns results to LLM
        #   4. LLM reasons about tool results and formulates response
        #   5. Loop repeats if more tools are needed
        print("\nSupportBot: ", end="", flush=True)
        response = agent(user_input)
        print()
        print()


if __name__ == "__main__":
    main()
