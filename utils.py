# utils.py (UPDATED for openai-python >= 1.0.0 + Streamlit secrets fallback)
import os
import json
import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st  # 👈 added

load_dotenv()

VECTOR_DIR = "vectors"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
DOCS_PATH = os.path.join(VECTOR_DIR, "docs.jsonl")
EMBED_MODEL = "text-embedding-3-small"


def get_openai_client():
    """
    Create OpenAI client using either local .env or Streamlit secrets.
    """
    key = (
        os.getenv("OPENAI_API_KEY")
        or st.secrets.get("OPENAI_API_KEY")  # 👈 fallback for Streamlit Cloud
    )
    if not key:
        raise RuntimeError(
            "No OPENAI_API_KEY set. Please set it in .env (local) or Streamlit secrets (cloud)."
        )
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
