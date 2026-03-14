"""
Module 4: Memory, Context & Token Management
==============================================
Add memory capabilities to the agent for personalized support.

This demonstrates:
- Conversation history (built-in session memory)
- Custom persistent memory (customer preferences)
- Context window management and token strategies
- Hierarchical context loading patterns (Skills.md approach)

Usage:
    python module_03_memory/agent_with_memory.py
"""

import sys
import os
import json
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from shared.data import ORDERS, PRODUCTS, FAQ

# ──────────────────────────────────────────────
# Persistent Memory Store
# ──────────────────────────────────────────────
# In production, this would use AgentCore Memory or a database.
# Here we use a simple JSON file to demonstrate the concept.

MEMORY_FILE = Path(__file__).parent / "customer_memory.json"


def load_memory() -> dict:
    """Load customer memory from persistent storage."""
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {}


def save_memory(memory: dict):
    """Save customer memory to persistent storage."""
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))


# ──────────────────────────────────────────────
# Memory-Aware Tools
# ──────────────────────────────────────────────


@tool
def remember_customer_preference(customer_id: str, key: str, value: str) -> dict:
    """Store a customer preference or note for future interactions.

    Args:
        customer_id: The customer identifier (e.g., email or name).
        key: The preference key (e.g., 'preferred_contact', 'product_interests').
        value: The preference value to remember.

    Returns:
        Confirmation that the preference was stored.
    """
    customer_id = customer_id.strip().lower()
    memory = load_memory()
    if customer_id not in memory:
        memory[customer_id] = {}
    memory[customer_id][key] = value
    save_memory(memory)
    return {"stored": True, "customer_id": customer_id, "key": key, "value": value}


@tool
def recall_customer_info(customer_id: str) -> dict:
    """Recall all stored information about a customer.

    Args:
        customer_id: The customer identifier to look up.

    Returns:
        All stored preferences and notes for this customer.
    """
    customer_id = customer_id.strip().lower()
    memory = load_memory()
    if customer_id in memory:
        return {"found": True, "customer_id": customer_id, "preferences": memory[customer_id]}
    return {"found": False, "message": f"No stored information for {customer_id}"}


@tool
def lookup_order(order_id: str) -> dict:
    """Look up a customer order by its order ID.

    Args:
        order_id: The order ID to look up (e.g., ORD-10001).
    """
    order_id = order_id.upper().strip()
    if order_id in ORDERS:
        return {"found": True, "order": ORDERS[order_id]}
    return {"found": False, "message": f"No order found with ID {order_id}"}


@tool
def search_faq(question: str) -> list[dict]:
    """Search the FAQ knowledge base.

    Args:
        question: The customer's question to search for.
    """
    question_lower = question.lower()
    results = []
    for faq_entry in FAQ:
        if any(word in faq_entry["question"].lower() or word in faq_entry["answer"].lower()
               for word in question_lower.split() if len(word) > 3):
            results.append(faq_entry)
    return results[:3] if results else [{"message": "No FAQ entries found."}]


@tool
def search_products(query: str) -> list[dict]:
    """Search the product catalog.

    Args:
        query: Search term to match against product names.
    """
    query_lower = query.lower()
    results = []
    for sku, product in PRODUCTS.items():
        if query_lower in product["name"].lower() or query_lower in product["description"].lower():
            results.append({"sku": sku, **product})
    return results if results else [{"message": f"No products found matching '{query}'"}]


# ──────────────────────────────────────────────
# Hierarchical Context Pattern
# ──────────────────────────────────────────────
# Instead of loading everything into the system prompt (wastes tokens),
# we use a tiered approach:
#
# Level 1 (Always loaded): Core personality + tool descriptions
# Level 2 (Loaded on demand): Detailed policies via FAQ tool
# Level 3 (External): Product catalog, orders (via tool calls)
#
# This mirrors the Skills.md pattern where SKILL.md frontmatter
# is always visible, but full instructions load only when needed.

SYSTEM_PROMPT = """You are SupportBot, a friendly customer support agent for TechStore.

## Your Capabilities
- Look up orders and their status
- Search products in the catalog
- Answer common questions from the FAQ
- Remember customer preferences for personalized service
- Recall past interactions with returning customers

## Memory Guidelines
- When a customer shares preferences (contact method, interests, etc.), remember them
- At the start of a conversation, try to recall if you know this customer
- Use remembered preferences to personalize responses
- If a customer mentions their name or email, use it as their customer_id

## Context Management
- Use search_faq for policy questions instead of guessing
- Use lookup_order for specific order queries
- Use search_products for catalog questions
- Only load detailed information when needed (don't dump everything)

## Token Efficiency Tips (for developers reading this)
- This system prompt is ~200 tokens (Level 1 context)
- FAQ entries load only when search_faq is called (Level 2)
- Full order/product details load only on lookup (Level 3)
- Customer memory loads only for known customers
- This keeps the context window lean for each interaction"""


# ──────────────────────────────────────────────
# Create Memory-Aware Agent
# ──────────────────────────────────────────────
agent = Agent(
    system_prompt=SYSTEM_PROMPT,
    tools=[
        lookup_order,
        search_products,
        search_faq,
        remember_customer_preference,
        recall_customer_info,
    ],
)


def main():
    print("=" * 60)
    print("  SupportBot with Memory - AI Customer Support Agent")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()
    print("  Try: 'Hi, I'm Alice. I love electronics products.'")
    print("  Try: 'What do you remember about Alice?'")
    print("  Try: 'What's your return policy?'")
    print()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nSupportBot: Thanks for chatting! Have a great day!")
            break
        if not user_input:
            continue

        print("\nSupportBot: ", end="", flush=True)
        response = agent(user_input)
        print()
        print()


if __name__ == "__main__":
    main()
