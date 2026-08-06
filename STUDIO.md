# LangGraph Studio — walkthrough

**What it is:** a visual IDE for your LangGraph agents. You run your graph locally with
`langgraph dev`; Studio renders it, lets you **submit inputs, watch each node execute,
inspect the state, and fork / replay** from any step. It's the debugger for agents.

**When to use it:** while *developing* a graph — to see *why* it behaves the way it does.
(For durable tracing across every run in production, that's LangSmith/Langfuse.)

---

## 1 · Prerequisites
- A recent CLI: **`langgraph-cli[inmem]` ≥ 0.2** (older 0.1.x has **no `dev` command**).
  ```bash
  pip install -U "langgraph-cli[inmem]"
  langgraph --version        # want >= 0.2 (this repo verified on 0.4.x)
  ```
- A browser with internet. The Studio **UI is hosted at smith.langchain.com** and connects
  back to your **local** server — so you'll likely need to be signed into a **free LangSmith
  account** to load the UI. *(Your graph still runs 100% locally; no API key needed.)*

## 2 · Launch
From the repo root, with your venv active:
```bash
langgraph dev
```
It reads [`langgraph.json`](langgraph.json) → loads the `agent` graph from
[`demos/studio_app/graph.py`](demos/studio_app/graph.py), and prints:
```
🚀 API:      http://127.0.0.1:2024
🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```
It usually opens the browser automatically; if not, click the **Studio UI** link.

## 3 · What you'll see
- The graph rendered as nodes + edges: **`__start__ → model → tools → model → __end__`**
  (the ReAct loop).
- An input box to submit a message to the agent.

## 4 · The live demo (do these in order)
1. **Submit a query:** *"How many Hauler units are in stock, and what's the total value?"*
2. **Watch it flow:** highlight the path `model → tools → model` — the reason→act→observe loop.
3. **Inspect state:** click the **`tools`** node → see the exact tool call + result; click
   **`model`** → see the messages. This is the "what did the agent actually do" view.
4. **Fork & replay (time-travel):** pick an earlier step, **edit the state** (e.g. change the
   tool result), and **re-run from there** — watch the final answer change. This is Studio's
   superpower: you don't restart, you branch from any point.
5. *(Optional)* **Add a breakpoint / interrupt** to pause before a node and approve — the
   visual version of the human-in-the-loop cell in notebook 02.

## 5 · Talking points
- *"Claude can generate this graph in seconds — Studio is for the 90% that's harder:
  knowing **why** it misbehaves on a real input."*
- *"Studio is a **visual trace you can poke at** while building; LangSmith is **durable
  tracing across every run**. Same plumbing — dev view vs. operator view."*
- *"Notice we didn't attach a checkpointer in `graph.py` — the dev server provides
  persistence, which is what makes fork/replay possible."*

## 6 · Troubleshooting
| Symptom | Fix |
|---|---|
| `Error: No such command 'dev'` | CLI too old — `pip install -U "langgraph-cli[inmem]"` |
| Studio UI won't load | Sign into a free LangSmith account; use **Chrome/Edge** |
| Browser blocks the local server | run `langgraph dev --tunnel` (routes through a secure tunnel) |
| `LangChain metadata … 403` in logs | Harmless — it's an optional telemetry ping; the graph runs fine |
| Port already in use | `langgraph dev --port 2025` |
| Graph fails to import | make sure your `.env` has `BASE_URL` + `API_KEY` set |

> **Backup for the live demo:** Studio depends on a browser + internet. Record a 60-sec
> screen capture of the fork/replay tonight so you can narrate it if the room wifi fails.
