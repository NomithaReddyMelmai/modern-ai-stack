"""
DEMO 2 — LangGraph: stateful agents.

Sections: (1) state graph from scratch, (2) conditional edges,
(3) prebuilt ReAct agent, (4) memory, (5) human-in-the-loop, (6) streaming.

Run:  python demos/02_langgraph.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypedDict, Literal
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from config import get_langchain_llm, assert_key

assert_key()
llm = get_langchain_llm()

# 1) State graph from scratch: nodes are functions over a shared state
class State(TypedDict):
    topic: str
    draft: str
    critique: str

def write(state: State) -> dict:
    return {"draft": llm.invoke(f"Write a one-sentence product tagline about: {state['topic']}").content}

def critique(state: State) -> dict:
    return {"critique": llm.invoke(f"Critique this tagline in one short line: {state['draft']}").content}

g = StateGraph(State)
g.add_node("write", write)
g.add_node("critique", critique)
g.add_edge(START, "write")
g.add_edge("write", "critique")
g.add_edge("critique", END)
app = g.compile()
r = app.invoke({"topic": "a warehouse security robot"})
print("\n--- 1) State graph ---")
print("DRAFT   :", r["draft"])
print("CRITIQUE:", r["critique"])

# 2) Conditional edges: a router picks the next node
class RouteState(TypedDict):
    question: str
    answer: str

def router(state: RouteState) -> Literal["math", "chat"]:
    return "math" if any(ch.isdigit() for ch in state["question"]) else "chat"

g2 = StateGraph(RouteState)
g2.add_node("classify", lambda s: {})
g2.add_node("math", lambda s: {"answer": "→ MATH branch"})
g2.add_node("chat", lambda s: {"answer": "→ CHAT branch"})
g2.add_edge(START, "classify")
g2.add_conditional_edges("classify", router, {"math": "math", "chat": "chat"})
g2.add_edge("math", END)
g2.add_edge("chat", END)
app2 = g2.compile()
print("\n--- 2) Conditional edges ---")
print(app2.invoke({"question": "What is 12 * 4?"})["answer"])
print(app2.invoke({"question": "Tell me about robots"})["answer"])

# tools for the agent sections
@tool
def inventory(sku: str) -> int:
    """Units in stock for a product SKU (scout/hauler/sentinel)."""
    return {"scout": 12, "hauler": 3, "sentinel": 0}.get(sku.lower(), 0)

@tool
def price(sku: str) -> int:
    """List price in USD for a product SKU."""
    return {"scout": 18000, "hauler": 42000, "sentinel": 30000}.get(sku.lower(), 0)

# 3) Prebuilt ReAct agent: the reason->act->observe loop, automated
agent = create_agent(llm, tools=[inventory, price])
print("\n--- 3) ReAct agent ---")
print(agent.invoke({"messages": [("user", "How many Hauler units, and total value?")]})["messages"][-1].content)

# 4) Memory: a checkpointer + thread_id remembers the conversation
mem = create_agent(llm, tools=[inventory, price], checkpointer=MemorySaver())
cfg = {"configurable": {"thread_id": "demo-1"}}
print("\n--- 4) Memory ---")
print(mem.invoke({"messages": [("user", "How many Hauler units do we have?")]}, cfg)["messages"][-1].content)
print(mem.invoke({"messages": [("user", "And the Scout?")]}, cfg)["messages"][-1].content)   # from memory

# 5) Human-in-the-loop: pause before running tools, then approve
hitl = create_agent(llm, tools=[inventory, price], checkpointer=MemorySaver(), interrupt_before=["tools"])
cfg2 = {"configurable": {"thread_id": "approval-1"}}
hitl.invoke({"messages": [("user", "How many Sentinel units are in stock?")]}, cfg2)
print("\n--- 5) Human-in-the-loop ---")
print("paused before:", hitl.get_state(cfg2).next)
print("approved     :", hitl.invoke(None, cfg2)["messages"][-1].content)

# 6) Streaming: watch the graph advance node by node
print("\n--- 6) Streaming steps ---")
for chunk in agent.stream({"messages": [("user", "What's the price of the Scout?")]}, stream_mode="updates"):
    print("step:", list(chunk.keys()))
