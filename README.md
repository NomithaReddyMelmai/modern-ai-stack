# Building AI Agents with LangChain & LangGraph
### Hands-on workshop — runbook

**Focus:** two tools, deep. **LLM gateway:** one OpenAI-compatible endpoint (LiteLLM Proxy or OpenRouter). **Format:** Jupyter notebooks + a live Studio peek.

---

## The story (say this up front)

> *"An LLM is a stateless, one-shot text predictor. Today we turn it into an **agent** —
> something that loops, uses tools, remembers, branches, and can pause for a human.
> **LangChain** gives us the building blocks; **LangGraph** makes them an agent."*

---

## Setup
Attendees follow [`SETUP.md`](SETUP.md) (do it *before* the session). Quick version:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in BASE_URL + API_KEY (+ model aliases)
python smoke_test.py          # must be all-green
```
One gateway powers everything — see the two blocks in [`.env.example`](.env.example)
(LiteLLM Proxy recommended for teams; OpenRouter as the solo alternative).

---

## 90-minute flow

| Min | Segment | Where |
|----:|---|---|
| 0–10 | Why a framework: a prompt isn't an agent | slides 1–3 |
| 10–35 | **LangChain**: LCEL, tool calling, streaming | notebook 01 |
| 35–45 | **The bridge**: the manual tool loop → why LangGraph | slide 5 (LangChain vs LangGraph) |
| 45–80 | **LangGraph**: state graph, conditional edges, ReAct agent, memory, human-in-the-loop | notebook 02 |
| 80–90 | **LangGraph Studio** peek + recap + Q&A | `langgraph dev` |

Deck: [`LangChain_LangGraph_Workshop.pptx`](LangChain_LangGraph_Workshop.pptx) (9 slides).

---

## The hands-on notebooks (the main event)

Run top to bottom; each ends with a **🧪 Your turn** exercise. Launch with `jupyter lab`,
kernel = **`Python (modern-ai-stack .venv)`**.

### ▶ Notebook 01 — LangChain ([`notebooks/01_langchain.ipynb`](notebooks/01_langchain.ipynb))
- **LCEL** — `prompt | model | parser`; `.invoke` / `.stream`
- **Tool calling** — the model *requests* a tool; **you** execute it and feed the result back
- **The catch** — a cell that closes the loop to a final answer
- **Say:** *"The model can't run code — it only asks. Closing that loop by hand is exactly what LangGraph automates."*

### ▶ Notebook 02 — LangGraph ([`notebooks/02_langgraph.ipynb`](notebooks/02_langgraph.ipynb))
1. **State graph from scratch** — nodes/edges over a shared state (`write → critique`)
2. **Conditional edges** — a router branches the path
3. **ReAct agent** — `create_agent` runs the reason→act→observe loop for you
4. **Memory** — checkpointer + `thread_id`; the follow-up "And the Scout?" works from context
5. **Human-in-the-loop** — `interrupt_before=["tools"]` pauses for approval, then resumes
- **Say:** *"This is the manual loop from notebook 1 — automated, with state, branching, and an approval gate."*

### ▶ LangGraph Studio (live, terminal)
```bash
langgraph dev
```
Opens the visual IDE for the graph in [`demos/studio_app/graph.py`](demos/studio_app/graph.py).
Submit a query → watch **agent → tools → agent** flow, open a node to inspect **state**,
then **fork & replay** from a step.
- **Say:** *"Codegen writes the graph; Studio + tracing tell you if it actually works."*

> Standalone scripts (same code, if you prefer a terminal to notebooks):
> [`demos/01_langchain.py`](demos/01_langchain.py), [`demos/02_langgraph.py`](demos/02_langgraph.py).

---

## Land the plane
- **LangChain** = the pieces (models, prompts, tools, LCEL).
- **LangGraph** = the runtime that loops, keeps state, branches, and pauses for humans.
- **One-liner:** *"Chains flow one way; agents loop, remember, branch, and pause for you."*

## Safety net
- Re-run `python smoke_test.py` ~10 min before you start, on the room wifi.
- Pre-open a JupyterLab tab and a terminal for `langgraph dev`.
- If `langgraph dev` is flaky on 3.13, use a 3.11/3.12 venv (or show a recorded clip).

## Troubleshooting
See [`SETUP.md`](SETUP.md#troubleshooting).
