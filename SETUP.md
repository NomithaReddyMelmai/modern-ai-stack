# Workshop Setup — do this BEFORE the session ⏱️ ~10 min

Hands-on session: **Building AI Agents with LangChain & LangGraph**.
Please arrive with a **green pre-flight** — we will *not* have time to install live.

---

## 1. Prerequisites
- **Python 3.11 or 3.12** (3.13 mostly works, but 3.11/3.12 is safest for `langgraph dev`)
- Git, and a terminal you're comfortable with

Check Python:
```bash
python3 --version      # want 3.11.x or 3.12.x
```

## 2. Get the code
```bash
git clone <REPO_URL>
cd modern-ai-stack        # or the folder name after cloning
```

## 3. Create a virtual env + install
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -U pip
pip install -r requirements.txt    # a few minutes
```

## 4. Get your gateway credentials
One OpenAI-compatible gateway powers both tools. Use whichever your host provides:

**LiteLLM Proxy (our team gateway):** you'll get a **base URL** and a **virtual key**
(`sk-...`) in **[your channel — e.g. Slack #ai-workshop]**. You'll also need the
**model aliases** the proxy exposes (e.g. `claude-sonnet`, `gpt-4o-mini`).

*(Alternative — OpenRouter: create a key at https://openrouter.ai/keys and add ~$5 credit.)*

## 5. Add your credentials
```bash
cp .env.example .env
```
Open `.env`, keep the **LiteLLM Proxy** block, and fill in `BASE_URL`, `API_KEY`,
and the `SMART_MODEL` / `FAST_MODEL` aliases. **Never commit this file** (git-ignored).

## 6. Pre-flight — the one thing that must pass ✅
```bash
python smoke_test.py
```
Verifies your key, does a live completion, and checks the LangChain + LangGraph imports.
**You want all-green.**

Expected tail:
```
✅ API key found
-> READY
✅ import langchain
✅ import langchain_openai
✅ import langgraph
All set. 🚀
```

## 7. Launch the hands-on notebooks
The workshop is driven from Jupyter notebooks in `notebooks/`:
```bash
jupyter lab
```
Open `notebooks/01_langchain.ipynb`, confirm the kernel is
**`Python (modern-ai-stack .venv)`** (top-right), and run top to bottom. Each notebook
ends with a **🧪 Your turn** exercise — that's the hands-on part.

---

## Troubleshooting
| Symptom | Fix |
|---|---|
| `No API key set` | You skipped step 5 — `cp .env.example .env` and set `BASE_URL` + `API_KEY` |
| 401 / auth error | Key typo, wrong `BASE_URL`, or (OpenRouter) no credit |
| Model not found / 404 | `SMART_MODEL` / `FAST_MODEL` must match an alias your gateway exposes |
| `403 Forbidden ... smith.langchain.com` | LangSmith tracing is on without a real key — set `LANGSMITH_TRACING=false` in `.env`, restart the kernel. Output is unaffected. |
| Notebook shows no output | Wrong kernel — pick **`Python (modern-ai-stack .venv)`**, then Restart Kernel & Run All |
| `langgraph dev` → `No such command 'dev'` | CLI too old — `pip install -U "langgraph-cli[inmem]"` |
| Studio UI won't load | Sign into a free LangSmith account; use Chrome/Edge. See [`STUDIO.md`](STUDIO.md) |
| `langgraph dev` still won't start | Use a Python 3.11/3.12 venv |

**Stuck? Reply to the invite before the session** so we can sort it out in advance —
not during. See you there! 🙌
