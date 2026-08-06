"""
Shared configuration for the Modern AI Stack workshop.

GATEWAY-AGNOSTIC: every tool talks to ONE OpenAI-compatible endpoint.
Works with either:
  • OpenRouter          (BASE_URL=https://openrouter.ai/api/v1)
  • a LiteLLM Proxy      (BASE_URL=https://<your-litellm-host>/v1)
...just by editing .env — no code changes.

Split:
  • Chat/LLM  -> the gateway (BASE_URL + API_KEY)
  • Embeddings-> LOCAL HuggingFace model (needs no gateway; always works)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# --- Gateway (any OpenAI-compatible endpoint). New names first, old ones as fallback. ---
BASE_URL = (os.environ.get("BASE_URL")
            or os.environ.get("OPENROUTER_BASE_URL")
            or "https://openrouter.ai/api/v1")
API_KEY = os.environ.get("API_KEY") or os.environ.get("OPENROUTER_API_KEY", "")

# --- Model names ---
# For OpenRouter these are provider slugs ("openai/gpt-4o-mini").
# For a LiteLLM proxy these are the ALIASES your proxy exposes ("gpt-4o-mini").
FAST_MODEL = os.environ.get("FAST_MODEL", "openai/gpt-4o-mini")   # cheap: multi-agent loops
SMART_MODEL = os.environ.get("SMART_MODEL", "anthropic/claude-sonnet-4.5")  # quality: hero demos

# LiteLLM-based tools (DSPy, CrewAI) treat the gateway as a generic OpenAI
# endpoint: "openai/<model>" + api_base=BASE_URL. Works for BOTH gateways.
FAST_MODEL_LITELLM = f"openai/{FAST_MODEL}"
SMART_MODEL_LITELLM = f"openai/{SMART_MODEL}"

# Local embedding model — runs on the laptop, no API key, ~90MB download once.
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---- Backward-compatible aliases (so older demos keep importing cleanly) ----
OPENROUTER_BASE_URL = BASE_URL
OPENROUTER_API_KEY = API_KEY


def get_langchain_llm(model: str = SMART_MODEL, temperature: float = 0.0):
    """LangChain / LangGraph / LangServe / LangMem chat model via the gateway."""
    from langchain_openai import ChatOpenAI
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        base_url=BASE_URL,
        api_key=API_KEY,
    )


def get_langchain_embeddings():
    """Local embeddings for LangChain (needs no gateway)."""
    from langchain_huggingface import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBED_MODEL)


def assert_key():
    if not API_KEY:
        raise SystemExit(
            "No API key set. Copy .env.example to .env and set API_KEY (or "
            "OPENROUTER_API_KEY) plus BASE_URL for your gateway."
        )
