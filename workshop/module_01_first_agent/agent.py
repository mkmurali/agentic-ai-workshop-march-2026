"""
Module 2: Your First Agent with Strands
=========================================
Build a simple customer support FAQ agent that can answer common questions.

This demonstrates:
- Creating a Strands Agent
- Using Amazon Bedrock as the model provider
- System prompts for agent behavior
- The agentic loop (reason → respond)

Usage:
    python module_01_first_agent/agent.py
"""

from strands import Agent

# ──────────────────────────────────────────────
# System Prompt - Defines the agent's personality and behavior
# ──────────────────────────────────────────────
SYSTEM_PROMPT = """You are SupportBot, a friendly and helpful customer support agent for TechStore,
an online electronics and accessories retailer.

Your responsibilities:
- Answer customer questions about products, orders, shipping, and returns
- Be polite, concise, and helpful
- If you don't know an answer, say so honestly and suggest contacting human support
- Never make up order details or tracking information

Company policies:
- 30-day return policy for unused items
- 90-day return for defective items
- Free shipping on orders over $100
- Standard shipping: 5-7 business days
- Express shipping: 2-3 business days ($9.99)
- Support hours: Mon-Fri 9am-6pm EST

Always greet the customer warmly and ask how you can help if they haven't stated their issue."""

# ──────────────────────────────────────────────
# Create the Agent
# ──────────────────────────────────────────────
# The simplest possible agent: just a model + system prompt
# By default, Strands uses Amazon Bedrock with Claude Sonnet
agent = Agent(system_prompt=SYSTEM_PROMPT)


def main():
    print("=" * 60)
    print("  SupportBot - Your AI Customer Support Agent")
    print("  Type 'quit' to exit")
    print("=" * 60)
    print()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("\nSupportBot: Thanks for chatting! Have a great day!")
            break
        if not user_input:
            continue

        # The agent processes the message through the agentic loop:
        #   1. Sends user message + system prompt to the LLM
        #   2. LLM reasons about the best response
        #   3. Returns the response (streaming by default)
        print("\nSupportBot: ", end="", flush=True)
        response = agent(user_input)
        print()  # newline after streamed response
        print()


if __name__ == "__main__":
    main()
