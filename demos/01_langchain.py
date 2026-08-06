"""
DEMO 1 — LangChain: the foundation (models, prompts, tools, LCEL chains).

Run:  python demos/01_langchain.py

Talking point: LangChain gives you a common interface over any model + a
composable way to wire prompts -> model -> parser (LCEL, the `|` operator),
plus tool-calling that every higher layer (LangGraph, CrewAI) builds on.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from config import get_langchain_llm, assert_key

assert_key()
llm = get_langchain_llm()

# 1) LCEL chain: prompt | model | parser
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant for AI engineers."),
    ("human", "Explain {topic} in exactly two sentences."),
])
chain = prompt | llm | StrOutputParser()
print("\n--- LCEL chain ---")
print(chain.invoke({"topic": "the difference between an LLM and an agent"}))

# 2) Tool calling — the primitive every agent framework relies on
@tool
def get_stock_level(sku: str) -> int:
    """Return the number of units in stock for a given product SKU."""
    return {"scout": 12, "hauler": 3, "sentinel": 0}.get(sku.lower(), 0)

llm_with_tools = llm.bind_tools([get_stock_level])
msg = llm_with_tools.invoke("How many Hauler units are in stock?")
print("\n--- Tool call requested by the model ---")
print(msg.tool_calls)

# 3) Streaming (great live — tokens appear in real time)
print("\n--- Streaming ---")
for chunk in chain.stream({"topic": "why observability matters for agents"}):
    print(chunk, end="", flush=True)
print()
