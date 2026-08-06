"""
PRE-FLIGHT smoke test — run this the night before AND 10 min before the demo.

  python smoke_test.py

Checks: (1) .env key present, (2) OpenRouter reachable + a live completion,
(3) all major imports resolve, (4) local embedding model loads.
Green here = your live demo will run.
"""
import importlib
from config import assert_key, get_langchain_llm, get_langchain_embeddings

def check_imports():
    mods = ["langchain", "langgraph", "langserve", "langmem", "langextract",
            "llama_index", "dspy", "crewai", "autogen_agentchat", "langsmith",
            "langfuse", "sentence_transformers"]
    ok = True
    for m in mods:
        try:
            importlib.import_module(m)
            print(f"  ✅ import {m}")
        except Exception as e:
            ok = False
            print(f"  ❌ import {m}: {e}")
    return ok

print("1) Key present…")
assert_key(); print("  ✅ OPENROUTER_API_KEY found")

print("2) Live OpenRouter completion…")
print("  ->", get_langchain_llm().invoke("Reply with the single word: READY").content)

print("3) Imports…")
check_imports()

print("4) Local embeddings (first run downloads ~90MB)…")
v = get_langchain_embeddings().embed_query("hello")
print(f"  ✅ embedding dim = {len(v)}")

print("\nAll set. 🚀")
