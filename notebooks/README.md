# Hands-on notebooks — LangChain & LangGraph

Run these **top to bottom**, then do the **🧪 Your turn** exercise at the end of each.
The finished code is your reference — the exercise is where you build.

## Launch
```bash
# from the repo root, with your venv active
jupyter lab
```
Open a notebook and make sure the kernel is **`Python (modern-ai-stack .venv)`**
(top-right kernel picker). Each notebook auto-adds the repo root to `sys.path`, so
`import config` just works.

## Order
| # | Notebook | Focus |
|---|---|---|
| 1 | `01_langchain.ipynb` | LCEL chains · streaming · tool calling |
| 2 | `02_langgraph.ipynb` | State graphs · ReAct agent · memory · conditional edges · human-in-the-loop |

## Also (run from a terminal)
- **LangGraph Studio** → `langgraph dev` — visualize the graph in `demos/studio_app/graph.py`,
  step through nodes, inspect state, fork & replay.
