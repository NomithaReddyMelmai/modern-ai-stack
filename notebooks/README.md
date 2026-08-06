# Hands-on notebooks

Run these **top to bottom**, then do the **🧪 Your turn** exercise at the end of each.
The finished code in each notebook is your reference — the exercise is where you build.

## Launch
```bash
# from the repo root, with your venv active
jupyter lab
```
Open a notebook, and make sure the kernel is your **`.venv`** (top-right kernel picker).
Each notebook auto-adds the repo root to `sys.path`, so `import config` just works.

## Order (matches the session)
| # | Notebook | Tool |
|---|---|---|
| 1 | `01_langchain.ipynb` | LangChain — foundation |
| 2 | `02_langgraph.ipynb` | LangGraph — stateful agent |
| 5 | `05_langmem.ipynb` | LangMem — long-term memory |
| 6 | `06_langextract.ipynb` | LangExtract — grounded extraction |
| 7 | `07_llamaindex.ipynb` | LlamaIndex — RAG |
| 8 | `08_dspy.ipynb` | DSPy — prompt optimization |
| 9 | `09_crewai.ipynb` | CrewAI — role-based multi-agent |
| 10 | `10_autogen.ipynb` | AutoGen — conversational multi-agent |
| 11 | `11_langsmith.ipynb` | LangSmith — tracing & eval |
| 12 | `12_langfuse.ipynb` | Langfuse — OSS observability |

## Not notebooks (run from a terminal — they start a server / UI)
- **3 · LangGraph Studio** → `langgraph dev` (opens the visual IDE in your browser)
- **4 · LangServe** → `python demos/04_langserve.py` (starts a REST API + playground)

See the top-level `README.md` for the exact steps and talking points for those two.
