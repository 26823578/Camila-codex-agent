
import os
import glob
import json
from pathlib import Path
from typing import List
from tqdm import tqdm
from dotenv import load_dotenv
import faiss
import numpy as np

#text extraction
from pypdf import PdfReader

# For embeddings
import openai

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
VECTOR_DIR = os.getenv("VECTOR_DIR", "./vectors")
CHUNK_SIZE = 450  # approx tokens per chunk
CHUNK_OVERLAP = 50

openai.api_key = OPENAI_API_KEY

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text.append(page_text)
    return "\n".join(text)

def read_file(path: str) -> str:
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(path)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

def chunk_text(text: str, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP) -> List[str]:
    sentences = sent_tokenize(text)
    chunks = []
    current = []
    current_len = 0
    for s in sentences:
        s_len = len(s.split())
        if current_len + s_len > chunk_size:
            chunks.append(" ".join(current))
            # keep overlap
            current = current[-overlap:] if overlap and len(current) >= overlap else []
            current_len = sum(len(x.split()) for x in current)
        current.append(s)
        current_len += s_len
    if current:
        chunks.append(" ".join(current))
    return chunks

def embed_texts(texts: List[str]) -> List[List[float]]:
    # batching
    embeddings = []
    for i in range(0, len(texts), 16):
        batch = texts[i:i+16]
        resp = openai.Embedding.create(model=EMBED_MODEL, input=batch)
        embeddings.extend([r["embedding"] for r in resp["data"]])
    return embeddings

def main():
    os.makedirs(VECTOR_DIR, exist_ok=True)
    docs = []
    meta = []
    for path in glob.glob("data/**", recursive=False):
        if Path(path).is_file():
            text = read_file(path)
            if not text.strip():
                continue
            chunks = chunk_text(text)
            for i, c in enumerate(chunks):
                docs.append(c)
                meta.append({"source": path, "chunk": i})
    print(f"Found {len(docs)} chunks. Creating embeddings...")
    embs = embed_texts(docs)
    dim = len(embs[0])
    xb = np.array(embs).astype("float32")
    index = faiss.IndexFlatL2(dim)
    index.add(xb)
    # persist
    faiss.write_index(index, os.path.join(VECTOR_DIR, "faiss.index"))
    with open(os.path.join(VECTOR_DIR, "docs.jsonl"), "w", encoding="utf-8") as f:
        for d, m in zip(docs, meta):
            f.write(json.dumps({"text": d, "meta": m}) + "\n")
    print("Ingest complete. Index stored at", VECTOR_DIR)

if __name__ == "__main__":
    main()
