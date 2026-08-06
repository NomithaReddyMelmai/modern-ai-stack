"""
DEMO 7 — LlamaIndex: RAG over your documents (the data/memory layer).

Run:  python demos/07_llamaindex.py

Talking point: LlamaIndex is the ingestion + retrieval engine — load docs,
chunk, embed, index, and query with citations. Note the split:
  LLM        -> OpenRouter (remote)
  Embeddings -> LOCAL HuggingFace  (OpenRouter has no embeddings endpoint)
"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from config import (OPENROUTER_API_KEY, OPENROUTER_BASE_URL, FAST_MODEL,
                    EMBED_MODEL, assert_key)

assert_key()

Settings.llm = OpenAILike(
    model=FAST_MODEL,
    api_base=OPENROUTER_BASE_URL,
    api_key=OPENROUTER_API_KEY,
    is_chat_model=True,
    is_function_calling_model=True,
    context_window=128000,
)
Settings.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
docs = SimpleDirectoryReader(data_dir).load_data()
index = VectorStoreIndex.from_documents(docs)     # embeds locally
qe = index.as_query_engine(similarity_top_k=3)

for q in ["How long are battery packs under warranty?",
          "What's the payload of the Hauler and its starting price?"]:
    print(f"\nQ: {q}")
    resp = qe.query(q)
    print("A:", resp)
    print("   sources:", [n.metadata.get("file_name") for n in resp.source_nodes])
