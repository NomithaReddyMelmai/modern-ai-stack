"""
DEMO 4 — LangServe: wrap a LangChain runnable as a REST API + playground.

Run:    python demos/04_langserve.py      (leave it running)
Open:   http://localhost:8000/support/playground/   (interactive UI)
Docs:   http://localhost:8000/docs                    (auto OpenAPI schema)

Curl it live (second terminal):
  curl -s http://localhost:8000/support/invoke \
       -H 'content-type: application/json' \
       -d '{"input": {"question": "What is the warranty on battery packs?"}}'

Talking point: LangServe wraps any runnable in FastAPI with /invoke, /stream,
/batch + a playground, for free. Best for simple chains; for stateful agents the
production path is LangGraph Platform (persistence, cron, webhooks).
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from langserve import add_routes
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import get_langchain_llm, assert_key
import uvicorn

assert_key()

chain = (
    ChatPromptTemplate.from_template(
        "You are Acme Robotics support. Answer the customer's question concisely.\n\n"
        "Question: {question}"
    )
    | get_langchain_llm()
    | StrOutputParser()
)

app = FastAPI(title="Acme Support — LangServe demo")
add_routes(app, chain, path="/support")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
