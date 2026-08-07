"""
Human-in-the-loop example for LangGraph Studio.

The agent PAUSES before running tools (`interrupt_before=["tools"]`). In Studio,
submit a question, watch it stop at the Interrupts panel, inspect the pending
tool call, then resume to approve.

NOTE: no checkpointer here — the dev server provides the persistence that makes
interrupts (and fork/replay) work.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_core.tools import tool
from langchain.agents import create_agent
from config import get_langchain_llm

llm = get_langchain_llm()


@tool
def inventory(sku: str) -> int:
    """Units in stock for a product SKU (scout/hauler/sentinel)."""
    return {"scout": 12, "hauler": 3, "sentinel": 0}.get(sku.lower(), 0)


@tool
def price(sku: str) -> int:
    """List price in USD for a product SKU."""
    return {"scout": 18000, "hauler": 42000, "sentinel": 30000}.get(sku.lower(), 0)


# Pause before the tool node — approve from the Studio "Interrupts" panel.
graph = create_agent(llm, tools=[inventory, price], interrupt_before=["tools"])
