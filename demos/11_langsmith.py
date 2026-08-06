"""
DEMO 11 — LangSmith: tracing + evaluation for the LangChain ecosystem.

Run:  python demos/11_langsmith.py
Then: open https://smith.langchain.com -> project "modern-ai-stack-demo"

Talking point: set 3 env vars (LANGSMITH_TRACING/API_KEY/PROJECT) and EVERY
LangChain + LangGraph run is traced automatically — full latency/token/cost
tree, nested tool calls, replay. `@traceable` extends this to ANY Python fn.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langsmith import traceable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_langchain_llm, assert_key

assert_key()
if os.environ.get("LANGSMITH_TRACING", "").lower() != "true":
    print("⚠️  LANGSMITH_TRACING is not 'true' — set it in .env to see traces.")

llm = get_langchain_llm()
chain = (ChatPromptTemplate.from_template("Summarize {topic} in one line.")
         | llm | StrOutputParser())

# 1) Auto-traced LangChain run (nothing extra needed)
print(chain.invoke({"topic": "vector databases"}))

# 2) @traceable brings your OWN functions into the same trace tree
@traceable(run_type="chain", name="two_step_pipeline")
def pipeline(topic: str) -> str:
    draft = chain.invoke({"topic": topic})
    polished = chain.invoke({"topic": f"rewrite more formally: {draft}"})
    return polished

print(pipeline("observability for AI agents"))
print("\n✅ Open LangSmith -> project 'modern-ai-stack-demo' to see the traces.")
