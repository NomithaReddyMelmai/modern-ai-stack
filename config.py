"""
Shared configuration for the Modern AI Stack workshop.

ONE key to rule them all: OpenRouter (OpenAI-compatible gateway).
- Chat/LLM  -> OpenRouter  (https://openrouter.ai/api/v1)
- Embeddings-> LOCAL HuggingFace model (OpenRouter has NO embeddings endpoint)

Import helpers from here in every demo so the config lives in one place.
"""
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# --- Model slugs (verify current slugs at https://openrouter.ai/models) ---
# Cheap + fast: good for multi-agent loops (CrewAI/AutoGen) so you don't burn credits.
FAST_MODEL = os.environ.get("FAST_MODEL", "openai/gpt-4o-mini")
# High quality: good for the "hero" single-agent demos.
SMART_MODEL = os.environ.get("SMART_MODEL", "anthropic/claude-sonnet-4.5")

# For LiteLLM-based tools (DSPy, CrewAI) prefix the slug with "openrouter/"
FAST_MODEL_LITELLM = f"openrouter/{FAST_MODEL}"
SMART_MODEL_LITELLM = f"openrouter/{SMART_MODEL}"

# Local embedding model — runs on your laptop, no API key, ~90MB download once.
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"


def get_langchain_llm(model: str = SMART_MODEL, temperature: float = 0.0):
    """LangChain / LangGraph / LangServe / LangMem chat model via OpenRouter."""
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        base_url=OPENROUTER_BASE_URL,
        api_key=OPENROUTER_API_KEY,
    )


def get_langchain_embeddings():
    """Local embeddings for LangChain (no OpenRouter embeddings endpoint exists)."""
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def assert_key():
    if not OPENROUTER_API_KEY:
        raise SystemExit(
            "OPENROUTER_API_KEY is not set. Copy .env.example to .env and add your key."
        )
