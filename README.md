# Building Production-Ready AI Agents with the Modern AI Stack
### Live-demo runbook — 90-minute hands-on workshop

**Audience:** senior AI/ML engineers · **LLM gateway:** OpenRouter (one key) · **Style:** copy-paste snippets + exact steps

---

## 0. The narrative (say this up front)

We build **one story** and each tool adds a production layer to it:

> *"We're building an internal agent for **Acme Robotics** — it answers product
> questions, remembers users, extracts structured data from docs, and is
> deployed, optimized, and fully observable."*

| Layer | Tool(s) | What it adds to the story |
|---|---|---|
| **Foundation** | LangChain | Model access, prompts, tools, chains (LCEL) |
| **Orchestration** | LangGraph | Stateful, looping agent as a graph |
| **Visual debug** | LangGraph Studio | See/step/replay the graph |
| **Deploy** | LangServe | Chain → REST API + playground |
| **Long-term memory** | LangMem | Facts that persist across sessions |
| **Structured extraction** | LangExtract | Grounded JSON from messy docs |
| **RAG / data** | LlamaIndex | Answer from Acme's documents |
| **Prompt optimization** | DSPy | Compile prompts instead of guessing |
| **Multi-agent (roles)** | CrewAI | Researcher → writer crew |
| **Multi-agent (chat)** | AutoGen | Writer ↔ critic conversation |
| **Observability (LC)** | LangSmith | Trace every run, evaluate |
| **Observability (OSS)** | Langfuse | Vendor-neutral tracing + costs |

**Reference architecture slide takeaway:** *LangChain/LangGraph = the runtime;
LlamaIndex + LangMem = the data/memory; DSPy = the compiler; CrewAI/AutoGen =
team topologies; LangServe/Studio = ship & debug; LangSmith/Langfuse = the eyes.*

---

## 1. Why OpenRouter is the right call here (say this at setup)

OpenRouter is an **OpenAI-compatible gateway** to ~hundreds of models with **one key**.
That lets every tool in this stack use the same credential:

- **OpenAI-compatible tools** (LangChain, LangGraph, LangServe, LangMem, LlamaIndex, AutoGen)
  → point an OpenAI client at `https://openrouter.ai/api/v1`.
- **LiteLLM-based tools** (DSPy, CrewAI) → just prefix the model: `openrouter/openai/gpt-4o-mini`.

### ⚠️ The one gotcha: embeddings
**OpenRouter has no embeddings endpoint.** RAG (LlamaIndex) needs embeddings, so we
run a **local HuggingFace model** (`all-MiniLM-L6-v2`) on the laptop — no second key,
works offline, and it makes a nice teaching point (remote LLM + local embeddings).

All of this lives in one place: [`config.py`](config.py).

---

## 2. One-time setup (do this the night before)

> Use **Python 3.11 or 3.12** if you can — a few of these libs lag on 3.13.

```bash
cd "Modern AI Stack"
python3 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt          # ~5–10 min; grab coffee

cp .env.example .env                      # then edit .env, paste your keys
```

Get free keys (all have generous free tiers):
- **OpenRouter** (required): https://openrouter.ai/keys — add a few $ of credit.
- **LangSmith**: https://smith.langchain.com → Settings → API Keys.
- **Langfuse**: https://cloud.langfuse.com → Project → Settings → API Keys.

### Pre-flight — run this and get all-green before you present
```bash
python smoke_test.py
```
It verifies your key, does a live completion, checks every import, and warms the
local embedding download. **Run it again 10 minutes before the session** (first run
downloads the embedding model + pulls models into OpenRouter cache).

---

## 3. 90-minute timing plan

| Min | Segment | Tools | Slides §|
|----:|---|---|---|
| 0–8 | Intro + the prototype→prod gap + stack map | — | 1–5 |
| 8–20 | Foundation & orchestration | LangChain, LangGraph | 6–8 |
| 20–30 | Visual debug + deploy | LangGraph Studio, LangServe | 9–10 |
| 30–42 | Memory & data | LangMem, LlamaIndex, LangExtract | 11–13 |
| 42–52 | Optimization | DSPy | 14 |
| 52–68 | Multi-agent | CrewAI, AutoGen | 15–16 |
| 68–82 | Observability | LangSmith, Langfuse | 17–18 |
| 82–90 | Fit-together architecture + Q&A | — | 19–21 |

Running long? The **droppable** demos are DSPy compile (show pre-recorded output)
and one of the two multi-agent frameworks. The **must-show** spine is
LangChain → LangGraph → LangServe → LlamaIndex → LangSmith.

---

## 4. The demos (run order = slide order)

Each block = **what to run**, **what to say**, **what they'll see**, **fallback**.

### ▶ Demo 1 — LangChain (foundation)
```bash
python demos/01_langchain.py
```
- **Say:** "One interface over any model. `prompt | model | parser` is LCEL — the
  composability primitive. And tool-calling here is what every agent framework builds on."
- **Show:** the LCEL answer, the `tool_calls` object, then live token streaming.
- **Fallback:** if streaming stalls, Ctrl-C — the first two prints already made the point.

### ▶ Demo 2 — LangGraph (stateful agent)
```bash
python demos/02_langgraph.py
```
- **Say:** "Chains are DAGs; agents need **loops** and **durable state**. `create_react_agent`
  gives us reason→act→observe with a checkpointer, so the 2nd question ('the Scout?')
  works from remembered context."
- **Show:** both answers; highlight that Q2 has no explicit subject — memory fills it in.

### ▶ Demo 3 — LangGraph Studio (visual debugging)
```bash
langgraph dev
```
- Opens a local server and a browser tab (LangGraph Studio UI). Pick the **`agent`** graph.
- **Say:** "This is the IDE for agents — the graph is rendered live."
- **Do live:** submit *"How many Hauler units and what's that worth?"* → watch it flow
  **agent → tools → agent**. Open a node to show **state**, then **fork/replay** from a step.
- **Fallback:** if the browser tab is blocked, the terminal prints a URL — paste it manually.
  If `langgraph dev` fails on 3.13, show the pre-recorded GIF (see §6).

### ▶ Demo 4 — LangServe (deploy as an API)
```bash
python demos/04_langserve.py      # leave it running
```
Then, in a second terminal / browser:
- Open **http://localhost:8000/joke/playground/** → type a topic → get output in a UI.
- Open **http://localhost:8000/docs** → the auto-generated OpenAPI schema.
- Curl it:
  ```bash
  curl -s http://localhost:8000/joke/invoke -H 'content-type: application/json' \
       -d '{"input": {"topic": "kubernetes"}}'
  ```
- **Say:** "Any runnable → `/invoke`, `/stream`, `/batch` + a playground, for free.
  For long-lived stateful agents, **LangGraph Platform** is the newer production path —
  LangServe is perfect for chains/services." (Stop the server with Ctrl-C after.)

### ▶ Demo 5 — LangMem (long-term memory)
```bash
python demos/05_langmem.py
```
- **Say:** "A checkpointer remembers a *thread*. LangMem extracts **durable facts**
  ('uses Python', 'wants type hints') you can reuse in a totally different session."
- **Show:** the bulleted extracted memories.

### ▶ Demo 6 — LangExtract (grounded structured extraction)
```bash
python demos/06_langextract.py
```
- **Say:** "Not just 'return JSON' — every field is **grounded to a source span**, so
  extractions are auditable. Killer for compliance/doc pipelines."
- **Show:** the extractions with `span=` offsets.
- **⚠️ Fallback (pre-flight this one!):** LangExtract routes `model_id`→provider by name
  and defaults to Gemini. If the OpenRouter override errors, use a **free Gemini key**
  (https://aistudio.google.com/apikey) with `model_id="gemini-2.0-flash"`. Details in the
  script's docstring.

### ▶ Demo 7 — LlamaIndex (RAG)
```bash
python demos/07_llamaindex.py
```
- **Say:** "Ingestion + retrieval engine. Note the split — **LLM is remote (OpenRouter),
  embeddings are local**. Answers come **with sources**."
- **Show:** both answers + the `sources:` line (grounded in `data/company_faq.md`).

### ▶ Demo 8 — DSPy (prompt optimization)
```bash
python demos/08_dspy.py
```
- **Say:** "Stop hand-tuning prompt strings. Declare I/O (a Signature) + a strategy
  (ChainOfThought); a **teleprompter compiles** few-shot demos against a metric.
  Prompts become optimized artifacts."
- **Show:** before/after answers, then `inspect_history` revealing the **auto-generated
  few-shot demos** DSPy attached. (Note: makes several calls — takes ~20–40s.)

### ▶ Demo 9 — CrewAI (role-based multi-agent)
```bash
python demos/09_crewai.py
```
- **Say:** "Model a **team**: each agent has a role/goal/backstory, tasks flow between them.
  Intuitive for researcher→writer→reviewer pipelines."
- **Show:** the `verbose` logs of the analyst then writer, then the final 4-bullet summary.

### ▶ Demo 10 — AutoGen (conversational multi-agent)
```bash
python demos/10_autogen.py
```
- **Say:** "Different topology — an async **conversation** until a termination condition.
  Writer and critic iterate until the critic says APPROVE. Note `model_info`: required to
  drive a non-OpenAI model (Claude via OpenRouter) through the OpenAI client."
- **Show:** the back-and-forth streaming in the console, ending on APPROVE.

### ▶ Demo 11 — LangSmith (observability, LangChain-native)
```bash
python demos/11_langsmith.py
```
- **Say:** "Three env vars and **every** LangChain/LangGraph run is traced — no code change.
  `@traceable` pulls your own functions into the same tree."
- **Do live:** open https://smith.langchain.com → project **modern-ai-stack-demo** →
  open a trace → expand the nested tool calls, show **latency / tokens / cost**.
  **Callback:** "Remember demo 2's agent loop? Re-run it now — it shows up here automatically."

### ▶ Demo 12 — Langfuse (observability, open-source)
```bash
python demos/12_langfuse.py
```
- **Say:** "The vendor-neutral, self-hostable counterpart. Same idea, works with **any**
  framework via a callback or `@observe`. Here we even attach a custom **score**."
- **Do live:** open https://cloud.langfuse.com → **Traces** → open the run → show the
  spans and the `length_ok` score.
- **Close the loop:** "LangSmith if you're all-in on LangChain; Langfuse if you want
  framework-agnostic + OSS/self-host. Both answer the production question: *what did my
  agent actually do, and what did it cost?*"

---

## 5. Land the plane (closing slides 19–21)

- **How they fit:** runtime (LangChain/LangGraph) · memory+data (LangMem/LlamaIndex/LangExtract)
  · compiler (DSPy) · team topologies (CrewAI/AutoGen) · ship+debug (LangServe/Studio) ·
  observability (LangSmith/Langfuse).
- **Production checklist:** eval before ship · trace everything · budget tokens/cost ·
  human-in-the-loop on risky tools · version prompts as artifacts · fail gracefully.
- **One-liner:** *"A prototype is a prompt; production is the stack around it."*

---

## 6. Safety net (do NOT skip)

- **Record every demo tonight** with `asciinema` or a screen recorder. If wifi/API dies
  live, play the recording and narrate. LangGraph Studio especially — capture a GIF.
- Keep a **second terminal** open (for LangServe + LangSmith you need two).
- Pre-open browser tabs: Studio, `localhost:8000/docs`, LangSmith project, Langfuse Traces.
- Have **credits** on OpenRouter (multi-agent demos burn tokens — that's why they use `FAST_MODEL`).
- If a specific model slug 404s, swap `SMART_MODEL`/`FAST_MODEL` in `.env` to any current
  slug from https://openrouter.ai/models (e.g. `openai/gpt-4o-mini`, `anthropic/claude-3.5-sonnet`).

## 7. Troubleshooting

| Symptom | Fix |
|---|---|
| `OPENROUTER_API_KEY is not set` | `cp .env.example .env`, paste key, re-run |
| 401 from OpenRouter | key typo / no credit on the account |
| Model 404 / not found | slug changed — pick a current one at openrouter.ai/models |
| Embedding download slow first run | expected (~90MB); pre-warm with `smoke_test.py` |
| No traces in LangSmith | `LANGSMITH_TRACING=true` and key set in `.env` (not just exported) |
| Langfuse empty | you must `get_client().flush()` before exit (script does this) |
| AutoGen `model_info` error | keep the full `model_info` dict (incl. `structured_output`) |
| `langgraph dev` fails on 3.13 | use a 3.11/3.12 venv, or show the recorded GIF |
| LangExtract errors on OpenRouter | fall back to a free Gemini key (see demo 6 docstring) |

---

**Files:** [`config.py`](config.py) · [`requirements.txt`](requirements.txt) ·
[`.env.example`](.env.example) · [`smoke_test.py`](smoke_test.py) · demos in [`demos/`](demos/)
