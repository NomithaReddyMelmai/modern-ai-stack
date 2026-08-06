"""
Graph exposed to LangGraph Studio via `langgraph dev`.

NOTE: do NOT attach a checkpointer here — the LangGraph dev server provides
persistence automatically. Studio will visualize this graph, let you step
through nodes, edit state, and re-run from any point.
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

graph = create_agent(llm, tools=[inventory, price])
