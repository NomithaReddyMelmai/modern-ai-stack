"""
A from-scratch StateGraph exposed to LangGraph Studio via `langgraph dev`.

Unlike the ReAct `agent` graph, this one shows explicit nodes/edges and a custom
state schema — so in Studio the input box asks for a `topic`, and you can watch
state flow `write -> critique`.

NOTE: no checkpointer here — the dev server provides persistence.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from config import get_langchain_llm

llm = get_langchain_llm()


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

graph = g.compile()   # <- Studio loads this
