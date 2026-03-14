"""
Module 3C: Agent Connected to MCP Server
==========================================
Connect the Strands agent to the MCP server for product catalog access.

This demonstrates:
- MCPClient for connecting to MCP servers
- stdio transport for local MCP servers
- Agent using tools from both @tool decorators and MCP servers
- The power of MCP: any agent can use any MCP-compatible tool server

Usage:
    python module_02_tools_mcp/agent_with_mcp.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client

from shared.data import FAQ

# ──────────────────────────────────────────────
# Connect to the MCP Server
# ──────────────────────────────────────────────
# The MCPClient connects to our product catalog MCP server
# using stdio transport (runs as a subprocess).
# MCPClient expects a callable that returns the transport (stdio_client(...)).
mcp_client = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="python",
            args=[os.path.join(os.path.dirname(os.path.abspath(__file__)), "mcp_server.py")],
        )
    )
)

# ──────────────────────────────────────────────
# Local tool (not from MCP) - FAQ search stays local
# ──────────────────────────────────────────────
from strands import tool


@tool
def search_faq(question: str) -> list[dict]:
    """Search the FAQ knowledge base for answers to common questions.

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


SYSTEM_PROMPT = """You are SupportBot, a helpful customer support agent for TechStore.

You have access to:
- Product catalog tools (via MCP): search_catalog, get_product_details, list_all_products, get_order_status
- FAQ search tool: search_faq

Always use the appropriate tool to look up information. Never make up data.
Be polite, concise, and accurate in your responses."""


def main():
    print("=" * 60)
    print("  SupportBot with MCP - AI Customer Support Agent")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()
    print("  Try: 'Show me all electronics products'")
    print("  Try: 'What's the status of order ORD-10002?'")
    print()

    # Use MCPClient as a context manager to manage the server lifecycle
    with mcp_client:
        # Get the tools provided by the MCP server
        mcp_tools = mcp_client.list_tools_sync()
        print(f"  Connected to MCP server. Available tools: {[t.tool_name for t in mcp_tools]}")
        print()

        # Create agent with both local tools and MCP tools
        agent = Agent(
            system_prompt=SYSTEM_PROMPT,
            tools=[search_faq, *mcp_tools],
        )

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
