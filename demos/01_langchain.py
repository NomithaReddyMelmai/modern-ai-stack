"""
DEMO 1 — LangChain: the foundation.

Sections: (1) LCEL chain, (2) streaming, (3) tool calling + closing the loop,
(4) structured output.

Run:  python demos/01_langchain.py
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from config import get_langchain_llm, assert_key

assert_key()
llm = get_langchain_llm()

# 1) LCEL chain: prompt | model | parser
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a concise assistant for AI engineers."),
    ("human", "Explain {topic} in exactly two sentences."),
])
chain = prompt | llm | StrOutputParser()
print("\n--- 1) LCEL chain ---")
print(chain.invoke({"topic": "the difference between an LLM and an agent"}))

# 2) Streaming (tokens appear live)
print("\n--- 2) Streaming ---")
for chunk in chain.stream({"topic": "why observability matters for agents"}):
    print(chunk, end="", flush=True)
print()

# 3) Tool calling — the model REQUESTS a tool; you execute it and feed it back
@tool
def get_stock_level(sku: str) -> int:
    """Return units in stock for a SKU. The sku is the lowercase product name, e.g. 'hauler'."""
    return {"scout": 12, "hauler": 3, "sentinel": 0}.get(sku.lower(), 0)

llm_with_tools = llm.bind_tools([get_stock_level])
q = "How many Hauler units are in stock?"
ai_msg = llm_with_tools.invoke(q)
print("\n--- 3) Tool calling ---")
print("requested:", ai_msg.tool_calls)          # the model's REQUEST (no result yet)

messages = [HumanMessage(q), ai_msg]
for tc in ai_msg.tool_calls:
    messages.append(get_stock_level.invoke(tc))  # run it -> ToolMessage (matched by id)
print("final   :", llm_with_tools.invoke(messages).content)

# 4) Structured output — force validated JSON (uses tool calling under the hood)
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(description="the product name")
    units_in_stock: int = Field(description="number of units in stock")

structured = llm.with_structured_output(Product)
print("\n--- 4) Structured output ---")
print(structured.invoke("The Acme Hauler currently has 3 units in stock."))
