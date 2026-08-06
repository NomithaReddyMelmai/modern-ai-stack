"""
DEMO 4 — LangServe: turn any LCEL chain / runnable into a REST API + playground.

Run:    python demos/04_langserve.py
Open:   http://localhost:8000/joke/playground/    (interactive UI)
Docs:   http://localhost:8000/docs                 (auto OpenAPI schema)

Curl it live:
  curl -s http://localhost:8000/joke/invoke \
       -H 'content-type: application/json' \
       -d '{"input": {"topic": "kubernetes"}}'

Talking point: LangServe wraps a runnable in FastAPI with /invoke, /stream,
/batch endpoints + a playground for free. (For long-lived stateful agents,
LangGraph Platform is the newer path — mention this as the production evolution.)
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
    ChatPromptTemplate.from_template("Tell a short, nerdy joke about {topic}.")
    | get_langchain_llm(temperature=0.7)
    | StrOutputParser()
)

app = FastAPI(title="Modern AI Stack — LangServe demo")
add_routes(app, chain, path="/joke")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
