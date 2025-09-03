# utils.py
import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from helpers import get_api_key   # <--- NEW

load_dotenv()

VECTOR_DIR = "vectors"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
DOCS_PATH = os.path.join(VECTOR_DIR, "docs.jsonl")
EMBED_MODEL = "text-embedding-3-small"

def get_openai_client():
    key = get_api_key()   # <--- USE HELPER
    if not key:
        raise RuntimeError("No OPENAI_API_KEY found. Set it in .env or Streamlit secrets.")
    return OpenAI(api_key=key)


def load_index():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCS_PATH):
        raise RuntimeError("Vector index or docs metadata not found. Please run ingest first.")
    
    index = faiss.read_index(INDEX_PATH)
    
    docs = []
    with open(DOCS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            docs.append(json.loads(line.strip()))
    
    return index, docs


def retrieve(query, k=4):
    """
    Retrieves top-k chunks for a given query.
    Returns list of dicts with {text, meta}.
    """
    # Load FAISS index and docs
    index, docs = load_index()

    # Get query embedding using new client
    client = get_openai_client()
    resp = client.embeddings.create(
        model=EMBED_MODEL,
        input=query
    )
    query_vec = np.array(resp.data[0].embedding, dtype=np.float32).reshape(1, -1)

    # Search in FAISS
    distances, indices = index.search(query_vec, k)
    
    results = []
    for idx in indices[0]:
        if idx < len(docs):
            results.append({
                "text": docs[idx]["text"],
                "meta": docs[idx]["meta"]
            })
    return results
