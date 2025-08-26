import os
import json
import faiss
import numpy as np

VECTOR_DIR = "vectors"
INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
DOCS_PATH = os.path.join(VECTOR_DIR, "docs.jsonl")

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
    import openai
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Load FAISS index and docs
    index, docs = load_index()

    # Get query embedding
    resp = openai.Embedding.create(
        model="text-embedding-3-small",
        input=query
    )
    query_vec = np.array(resp["data"][0]["embedding"], dtype=np.float32).reshape(1, -1)

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
