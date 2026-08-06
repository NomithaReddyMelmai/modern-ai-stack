# Workshop Setup — do this BEFORE the session ⏱️ ~15 min

Hands-on session: **Building Production-Ready AI Agents with the Modern AI Stack**.
Please arrive with a **green pre-flight** — we will *not* have time to install live.

---

## 1. Prerequisites
- **Python 3.11 or 3.12** (3.13 works for most tools but a couple lag — 3.11/3.12 is safest)
- Git, and a terminal you're comfortable with
- ~1 GB free disk (dependencies + a small local embedding model)

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
pip install -r requirements.txt    # 5–10 min; grab a coffee
```

## 4. Get your gateway credentials
One OpenAI-compatible gateway powers **every** tool. Use whichever your host provides:

**LiteLLM Proxy (our team gateway):** you'll get a **base URL** and a **virtual key**
(`sk-...`) in **[your channel — e.g. Slack #ai-workshop]**. Ask for your key if you
don't have one. You'll also need the **model aliases** the proxy exposes (e.g.
`claude-sonnet`, `gpt-4o-mini`).

*(Alternative — OpenRouter: create a key at https://openrouter.ai/keys and add ~$5 credit.)*

**Optional — observability demos only:**
| Key | Where |
|---|---|
| LangSmith | https://smith.langchain.com → Settings → API Keys |
| Langfuse | https://cloud.langfuse.com → Settings → API Keys |

> 💡 Embeddings run **locally** (HuggingFace) — no gateway needed for the RAG demo.

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
This verifies your key, does a live completion, checks every import, and downloads
the local embedding model (~90 MB, first run only). **You want all-green.**

Expected tail:
```
✅ OPENROUTER_API_KEY found
-> READY
✅ import langchain ... (all green)
✅ embedding dim = 384
All set. 🚀
```

---

## 7. Launch the hands-on notebooks
The workshop is driven from Jupyter notebooks in `notebooks/`:
```bash
jupyter lab
```
Open `notebooks/01_langchain.ipynb`, confirm the kernel is your **`.venv`** (top-right),
and run top to bottom. Each notebook ends with a **🧪 Your turn** exercise — that's the
hands-on part. See `notebooks/README.md` for the run order.

---

## Troubleshooting
| Symptom | Fix |
|---|---|
| `No API key set` | You skipped step 5 — `cp .env.example .env` and set `BASE_URL` + `API_KEY` |
| 401 / auth error | Key typo, wrong `BASE_URL`, or (OpenRouter) no credit |
| Model not found / 404 | `SMART_MODEL` / `FAST_MODEL` must match an alias your gateway exposes |
| `No module named autogen_agentchat` | `pip install -U "autogen-agentchat>=0.4" "autogen-ext[openai]"` |
| protobuf conflict warning | Harmless — ignore unless an import actually fails |
| Embedding download slow | Expected once (~90 MB); let it finish |
| `langgraph dev` won't start | Use a Python 3.11/3.12 venv |

**Stuck? Reply to the invite before the session** so we can sort it out in advance —
not during. See you there! 🙌
