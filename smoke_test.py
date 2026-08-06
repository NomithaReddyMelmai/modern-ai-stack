"""
PRE-FLIGHT smoke test — run the night before AND ~10 min before the session.

  python smoke_test.py

Checks: (1) API key present, (2) gateway reachable + a live completion,
(3) LangChain + LangGraph import. Green here = your live demo will run.
"""
import importlib
from config import assert_key, get_langchain_llm

print("1) Key present…")
assert_key(); print("  ✅ API key found")

print("2) Live gateway completion…")
print("  ->", get_langchain_llm().invoke("Reply with the single word: READY").content)

print("3) Imports…")
ok = True
for m in ["langchain", "langchain_openai", "langgraph"]:
    try:
        importlib.import_module(m)
        print(f"  ✅ import {m}")
    except Exception as e:
        ok = False
        print(f"  ❌ import {m}: {e}")

print("\nAll set. 🚀" if ok else "\nSome imports failed — see above.")
