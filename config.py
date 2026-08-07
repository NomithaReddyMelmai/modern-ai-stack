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

# --- Gateway (any OpenAI-compatible endpoint) ---
# We accept several env-var naming conventions so your .env "just works":
#   BASE_URL / API_KEY               (generic)
#   LITELLM_BASE_URL / LITELLM_API_KEY   (LiteLLM proxy)
#   OPENROUTER_BASE_URL / OPENROUTER_API_KEY  (OpenRouter fallback)
_env = os.environ.get
# LiteLLM mode = a LiteLLM proxy URL + key are both present.
_litellm_mode = bool(_env("LITELLM_BASE_URL") and _env("LITELLM_API_KEY"))

BASE_URL = (_env("BASE_URL") or _env("LITELLM_BASE_URL")
            or _env("OPENROUTER_BASE_URL") or "https://openrouter.ai/api/v1")
API_KEY = (_env("API_KEY") or _env("LITELLM_API_KEY")
           or _env("OPENROUTER_API_KEY", ""))

# --- Model names ---
# LiteLLM proxy: aliases it exposes (LLM_MODEL_ID / LLM_SMALLER_MODEL_ID).
# OpenRouter: provider slugs ("openai/gpt-4o-mini").
if _litellm_mode:
    # Prefer the proxy's own aliases; a leftover SMART_MODEL may hold an OpenRouter slug.
    SMART_MODEL = _env("LLM_MODEL_ID") or _env("SMART_MODEL") or "gpt-4o"
    FAST_MODEL = _env("LLM_SMALLER_MODEL_ID") or _env("FAST_MODEL") or "gpt-4o-mini"
else:
    SMART_MODEL = _env("SMART_MODEL") or _env("LLM_MODEL_ID") or "anthropic/claude-sonnet-4.5"
    FAST_MODEL = _env("FAST_MODEL") or _env("LLM_SMALLER_MODEL_ID") or "openai/gpt-4o-mini"

# LiteLLM-based tools (DSPy, CrewAI) treat the gateway as a generic OpenAI
# endpoint: "openai/<model>" + api_base=BASE_URL. Works for BOTH gateways.
FAST_MODEL_LITELLM = f"openai/{FAST_MODEL}"
SMART_MODEL_LITELLM = f"openai/{SMART_MODEL}"

# Local embedding model — runs on the laptop, no API key, ~90MB download once.
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Some reasoning models (e.g. gpt-5.x) reject tool-calling unless reasoning_effort
# is 'none'. Default to 'none' on a LiteLLM proxy so tools/agents work; leave unset
# for OpenRouter (non-reasoning models reject the param). Override via REASONING_EFFORT.
REASONING_EFFORT = _env("REASONING_EFFORT") or ("none" if _litellm_mode else None)

# ---- Backward-compatible aliases (so older demos keep importing cleanly) ----
OPENROUTER_BASE_URL = BASE_URL
OPENROUTER_API_KEY = API_KEY


def get_langchain_llm(model: str = SMART_MODEL, temperature: float = 0.0):
    """LangChain / LangGraph / LangServe / LangMem chat model via the gateway."""
    from langchain_openai import ChatOpenAI
    kwargs = dict(model=model, temperature=temperature, base_url=BASE_URL, api_key=API_KEY)
    if REASONING_EFFORT:                       # needed for tool-calling on reasoning models
        kwargs["reasoning_effort"] = REASONING_EFFORT
    return ChatOpenAI(**kwargs)


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
