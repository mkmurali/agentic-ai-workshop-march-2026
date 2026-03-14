# Agentic AI Workshop

A hands-on, 3-hour workshop for building agentic AI applications with **Strands Agents SDK** and **AWS AgentCore**.

## What You'll Build

**SupportBot** — A multi-agent customer support system featuring:
- Triage agent that routes to specialist agents (billing, technical, returns)
- Custom tools and MCP server for product catalog
- Persistent memory and hierarchical context management
- Evaluation suite, safety guardrails, and OpenTelemetry observability
- Production deployment on Amazon Bedrock AgentCore

## Project Structure

```
agentic-ai-workshops/
├── website/                    # Astro Starlight documentation site
├── workshop/                   # Python workshop code
│   ├── module_00_setup/        # Environment verification
│   ├── module_01_first_agent/  # Basic Strands agent
│   ├── module_02_tools_mcp/    # Custom tools + MCP server
│   ├── module_03_memory/       # Memory & context management
│   ├── module_04_multi_agent/  # Multi-agent triage system
│   ├── module_05_evals/        # Evals + safety + observability
│   ├── module_06_deploy/       # AgentCore deployment
│   └── shared/                 # Shared mock data
├── presentation/               # Reveal.js slide deck
└── README.md
```

## Quick Start

### Workshop Code

```bash
cd workshop
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python module_00_setup/verify_setup.py
```

### Documentation Site

```bash
cd website
npm install
npm run dev
```

### Presentation

```bash
cd presentation
npx serve .
```

## Prerequisites

- Python 3.12+
- Node.js 18+
- AWS account with Bedrock access (Claude Sonnet)
- AWS CLI configured

## Workshop Modules

| Module | File | Topic |
|--------|------|-------|
| 0 | `module_00_setup/verify_setup.py` | Setup & verification |
| 1 | `module_01_first_agent/agent.py` | Your first agent |
| 2a | `module_02_tools_mcp/tools.py` | Custom tools |
| 2b | `module_02_tools_mcp/mcp_server.py` | MCP server |
| 2c | `module_02_tools_mcp/agent_with_mcp.py` | Agent + MCP |
| 3 | `module_03_memory/agent_with_memory.py` | Memory & context |
| 4 | `module_04_multi_agent/triage_agent.py` | Multi-agent system |
| 5 | `module_05_evals/eval_suite.py` | Evals, safety, observability |
| 6 | `module_06_deploy/app.py` | AgentCore deployment |

## Tech Stack

- [Strands Agents SDK](https://strandsagents.com/) - Agent framework
- [Amazon Bedrock](https://aws.amazon.com/bedrock/) - Model provider
- [Amazon Bedrock AgentCore](https://aws.amazon.com/bedrock/agentcore/) - Deployment platform
- [Astro Starlight](https://starlight.astro.build/) - Documentation site
- [Reveal.js](https://revealjs.com/) - Presentation framework
