"""
DEMO 2 — LangGraph: stateful, cyclic agent as a graph (with memory + tools).

Run:  python demos/02_langgraph.py

Talking point: Chains are DAGs. Real agents need LOOPS (reason -> act -> observe
-> reason ...), durable state, and human-in-the-loop. LangGraph models the agent
as a graph with a checkpointer so runs are resumable and inspectable.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from config import get_langchain_llm, assert_key

assert_key()
llm = get_langchain_llm()

@tool
def inventory(sku: str) -> int:
    """Units in stock for a product SKU (scout/hauler/sentinel)."""
    return {"scout": 12, "hauler": 3, "sentinel": 0}.get(sku.lower(), 0)

@tool
def price(sku: str) -> int:
    """List price in USD for a product SKU."""
    return {"scout": 18000, "hauler": 42000, "sentinel": 30000}.get(sku.lower(), 0)

# A full ReAct agent (LLM + tools + loop) in one line, with a checkpointer
# so the same thread_id remembers the conversation.
agent = create_agent(llm, tools=[inventory, price], checkpointer=MemorySaver())
cfg = {"configurable": {"thread_id": "demo-thread-1"}}

def ask(q):
    print(f"\nUSER: {q}")
    out = agent.invoke({"messages": [("user", q)]}, cfg)
    print("AGENT:", out["messages"][-1].content)

ask("How many Hauler units do we have, and what's the total value of that stock?")
ask("And what about the Scout?")   # <- relies on checkpointed memory of context
