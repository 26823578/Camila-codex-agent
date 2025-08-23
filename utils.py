import os
import json
import numpy as np
import faiss
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
VECTOR_DIR = os.getenv("VECTOR_DIR", "./vectors")

openai.api_key = OPENAI_API_KEY

def load_index():
    index_path = os.path.join(VECTOR_DIR, "faiss.index")
    index = faiss.read_index(index_path)
    docs = []
    with open(os.path.join(VECTOR_DIR, "docs.jsonl"), "r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line))
    return index, docs

def embed_query(q):
    resp = openai.Embedding.create(model=EMBED_MODEL, input=q)
    return np.array(resp["data"][0]["embedding"], dtype="float32")

def retrieve(query, k=4):
    index, docs = load_index()
    q_emb = embed_query(query)
    D, I = index.search(np.array([q_emb]), k)
    results = []
    for idx in I[0]:
        results.append(docs[idx])
    return results
