"""
DEMO 5 — LangMem: long-term memory (extract durable facts from conversation).

Run:  python demos/05_langmem.py

Talking point: a checkpointer remembers a *thread*. LangMem gives agents
long-term memory ACROSS threads — it uses an LLM to extract, consolidate, and
update durable "memories" (user preferences, facts) you can inject later.
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langmem import create_memory_manager
from config import get_langchain_llm, assert_key

assert_key()

# The manager uses an LLM to turn raw conversation into structured memories.
manager = create_memory_manager(
    get_langchain_llm(),
    instructions="Extract durable facts and preferences about the user. "
                 "Ignore small talk.",
    enable_inserts=True,
)

conversation = [
    {"role": "user", "content": "Hey, I'm Priya, a platform engineer at Acme."},
    {"role": "user", "content": "We standardize on Python and deploy on GKE."},
    {"role": "user", "content": "Please always give me answers with type hints."},
]

memories = manager.invoke({"messages": conversation})
print("\n--- Extracted long-term memories ---")
for m in memories:
    print("•", m.content)

# In a real agent you'd store these (e.g. in a vector/store) and retrieve the
# relevant ones to prepend to the system prompt on future, unrelated threads.
