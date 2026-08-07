"""
Conditional-edges example for LangGraph Studio.

Shows branching: a router picks the next node based on the question.
In Studio the input box asks for a `question`; watch it route to math vs chat.

NOTE: no checkpointer here — the dev server provides persistence.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END


class RouteState(TypedDict):
    question: str
    answer: str


def router(state: RouteState) -> Literal["math", "chat"]:
    # deterministic (no LLM) so the branching is easy to see in Studio
    return "math" if any(ch.isdigit() for ch in state["question"]) else "chat"


def math_node(state: RouteState) -> dict:
    return {"answer": "→ routed to the MATH branch (a calculator agent would handle this)."}


def chat_node(state: RouteState) -> dict:
    return {"answer": "→ routed to the CHAT branch (a general agent would handle this)."}


g = StateGraph(RouteState)
g.add_node("classify", lambda s: {})           # entry
g.add_node("math", math_node)
g.add_node("chat", chat_node)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", router, {"math": "math", "chat": "chat"})
g.add_edge("math", END)
g.add_edge("chat", END)

graph = g.compile()   # <- Studio loads this
