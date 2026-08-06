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

## 4. Get your API keys (free tiers)
You need **one required** key and **two optional** ones.

| Key | Required? | Where | Notes |
|---|---|---|---|
| **OpenRouter** | ✅ Required | https://openrouter.ai/keys | Add **~$5 credit** — the multi-agent demos make many calls |
| LangSmith | Optional | https://smith.langchain.com → Settings → API Keys | For the tracing demo |
| Langfuse | Optional | https://cloud.langfuse.com → Settings → API Keys | For the OSS observability demo |

> 💡 One OpenRouter key powers **every** tool in the workshop. Embeddings run
> locally (no extra key needed).

## 5. Add your keys
```bash
cp .env.example .env
```
Open `.env` and paste your keys. **Never commit this file** (it's git-ignored).

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

## Troubleshooting
| Symptom | Fix |
|---|---|
| `OPENROUTER_API_KEY is not set` | You skipped step 5 — `cp .env.example .env` and paste your key |
| 401 from OpenRouter | Key typo, or no credit on the account |
| `No module named autogen_agentchat` | `pip install -U "autogen-agentchat>=0.4" "autogen-ext[openai]"` |
| protobuf conflict warning | Harmless — ignore unless an import actually fails |
| Embedding download slow | Expected once (~90 MB); let it finish |
| `langgraph dev` won't start | Use a Python 3.11/3.12 venv |

**Stuck? Reply to the invite before the session** so we can sort it out in advance —
not during. See you there! 🙌
