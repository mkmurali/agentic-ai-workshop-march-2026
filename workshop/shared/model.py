"""
Shared Model Configuration
============================
Single place to configure the LLM model used across all workshop modules.

Uncomment ONE of the model options below (and comment out the others) to switch
the model used across every module. Change it here once, and all modules pick it up.
"""

import os


# # ══════════════════════════════════════════════
# # Option 1: AWS Bedrock (default - Claude Sonnet)
# # ══════════════════════════════════════════════
# # Uses your AWS credentials (env vars, ~/.aws/credentials, or IAM role).
# # No API key needed if AWS is configured.
# #
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    max_tokens=1000,
    temperature=0.7,
)


# # ══════════════════════════════════════════════
# # Option 2: AWS Bedrock - different model (e.g. Claude Haiku for faster/cheaper responses)
# # ══════════════════════════════════════════════
# #
# # Uses your AWS credentials (env vars, ~/.aws/credentials, or IAM role).
# # No API key needed if AWS is configured.

# from strands.models.bedrock import BedrockModel
# model = BedrockModel(
#     model_id="us.anthropic.claude-haiku-4-5-20251001-v1:0",
#     region_name="us-east-1",
#     max_tokens=1000,
#     temperature=0.7,
# )


# # ══════════════════════════════════════════════
# # Option 3: OpenAI (GPT-4o, GPT-4o-mini, etc.)
# # ══════════════════════════════════════════════
# # Set your API key: export OPENAI_API_KEY="YOUR_KEY_HERE"
# # or os.environ["OPENAI_API_KEY"]="YOUR_KEY_HERE"

# from strands.models.openai import OpenAIModel
# model = OpenAIModel(
#     model_id="gpt-4o",
#     params={
#         "max_tokens": 1000,
#         "temperature": 0.7,
#     },
# )


# ══════════════════════════════════════════════
# Option 4: LiteLLM (unified interface to 100+ models)
# ══════════════════════════════════════════════
# Requires: pip install litellm
# LiteLLM supports OpenAI, Anthropic, Cohere, HuggingFace, Ollama, and more.
# See: https://docs.litellm.ai/docs/providers
#
# Example - Anthropic direct:
#   os.environ["ANTHROPIC_API_KEY"] = "YOUR_KEY_HERE"
#   model_id = "anthropic/claude-sonnet-4-20250514"
#
# Example - Ollama (local):
#   model_id = "ollama/llama3"
#
# from strands.models.litellm import LiteLLMModel
#
# model = LiteLLMModel(
#     model_id="anthropic/claude-sonnet-4-20250514",
#     params={
#         "max_tokens": 1000,
#         "temperature": 0.7,
#     },
# )


# # ══════════════════════════════════════════════
# # Option 5: OpenRouter via LiteLLM (access many models with one API key)
# # ══════════════════════════════════════════════
# # Get your key at https://openrouter.ai/keys
# # pip install 'strands-agents[litellm]' strands-agents-tools
# # export OPENROUTER_API_KEY="YOUR_KEY_HERE" or
# os.environ["OPENROUTER_API_KEY"] = "YOUR_KEY_HERE"

# from strands.models.litellm import LiteLLMModel
# model = LiteLLMModel(
#     model_id="openrouter/nvidia/nemotron-3-super-120b-a12b:free",
#     params={
#         "max_tokens": 1000,
#         "temperature": 0.7,
#     },
# )
