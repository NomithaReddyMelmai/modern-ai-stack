"""
DEMO 12 — Langfuse: open-source observability (works with ANY framework).

Run:  python demos/12_langfuse.py
Then: open https://cloud.langfuse.com -> Traces

Talking point: the vendor-neutral counterpart to LangSmith. Open source,
self-hostable, and framework-agnostic. Drop its callback into LangChain, or
wrap any function with @observe. Traces, costs, evals, prompt management.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langfuse import observe, get_client
from langfuse.langchain import CallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_langchain_llm, assert_key

assert_key()
handler = CallbackHandler()   # reads LANGFUSE_* from .env
chain = (ChatPromptTemplate.from_template("Give 3 risks of deploying agents in prod about {topic}.")
         | get_langchain_llm() | StrOutputParser())

# 1) LangChain run captured via the Langfuse callback
print(chain.invoke({"topic": "tool-calling agents"},
                   config={"callbacks": [handler]}))

# 2) @observe traces plain Python too (framework-agnostic)
@observe()
def scored_pipeline(topic: str) -> str:
    out = chain.invoke({"topic": topic}, config={"callbacks": [handler]})
    get_client().score_current_trace(name="length_ok", value=1 if len(out) < 800 else 0)
    return out

scored_pipeline("multi-agent orchestration")
get_client().flush()   # ensure events are sent before the script exits
print("\n✅ Open https://cloud.langfuse.com -> Traces to see both runs.")
