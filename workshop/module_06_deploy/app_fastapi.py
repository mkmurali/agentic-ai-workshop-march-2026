"""
Module 7 (Alternative): Deploy as FastAPI + Docker
====================================================
Deploy the SupportBot as a containerized FastAPI service.

This is an alternative to the AgentCore starter toolkit approach,
giving you full control over the HTTP interface.

Usage (local):
    uvicorn module_06_deploy.app_fastapi:app --host 0.0.0.0 --port 8080

Usage (Docker):
    docker build -t supportbot -f module_06_deploy/Dockerfile .
    docker run -p 8080:8080 supportbot
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from strands import Agent, tool
from shared.data import ORDERS, PRODUCTS, FAQ

app = FastAPI(title="SupportBot API", version="1.0.0")


# ──────────────────────────────────────────────
# Tools
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
        query: Search term.
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


# ──────────────────────────────────────────────
# Agent
# ──────────────────────────────────────────────

agent = Agent(
    system_prompt="You are SupportBot for TechStore. Use tools to look up data. Be concise and helpful.",
    tools=[lookup_order, search_products, search_faq],
)


# ──────────────────────────────────────────────
# API Endpoints (AgentCore compatible)
# ──────────────────────────────────────────────

class InvocationRequest(BaseModel):
    prompt: str
    session_id: str | None = None


class InvocationResponse(BaseModel):
    response: str
    session_id: str | None = None


@app.get("/ping")
async def health_check():
    """Health check endpoint required by AgentCore Runtime."""
    return {"status": "healthy"}


@app.post("/invocations", response_model=InvocationResponse)
async def invoke_agent(request: InvocationRequest):
    """Invoke the agent with a prompt. Compatible with AgentCore Runtime."""
    try:
        result = agent(request.prompt)
        response_text = result.message.content[0]["text"] if result.message.content else ""
        return InvocationResponse(
            response=response_text,
            session_id=request.session_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
