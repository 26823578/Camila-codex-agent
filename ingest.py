import os
import json
import faiss
import numpy as np
import openai
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx
import nltk

nltk.download('punkt')

from nltk.tokenize import sent_tokenize

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DATA_DIR = "data"
VECTOR_DIR = "vectors"
os.makedirs(VECTOR_DIR, exist_ok=True)

INDEX_PATH = os.path.join(VECTOR_DIR, "faiss.index")
DOCS_PATH = os.path.join(VECTOR_DIR, "docs.jsonl")

EMBED_MODEL = "text-embedding-3-small"

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def chunk_text(text, chunk_size=450, overlap=50):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = []
    tokens_in_chunk = 0

    for sent in sentences:
        tokens = len(sent.split())
        if tokens_in_chunk + tokens > chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = current_chunk[-overlap:] if overlap > 0 else []
            tokens_in_chunk = sum(len(s.split()) for s in current_chunk)
        current_chunk.append(sent)
        tokens_in_chunk += tokens

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def embed_text(texts):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    # OpenAI API accepts up to 2048 inputs per request for embeddings, but batching is safer for large sets
    batch_size = 64
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=batch
        )
        embeddings.extend([np.array(e.embedding, dtype=np.float32) for e in response.data])
    return embeddings

def main():
    print("Starting ingestion...")
    all_chunks = []
    metadata = []
    for filename in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR, filename)
        if filename.lower().endswith(".txt"):
            text = read_txt(path)
        elif filename.lower().endswith(".pdf"):
            text = read_pdf(path)
        elif filename.lower().endswith(".docx"):
            text = read_docx(path)
        else:
            print(f"Skipping unsupported file: {filename}")
            continue

        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            metadata.append({"source": filename, "chunk": i})

    print(f"Total chunks: {len(all_chunks)}")
    if not all_chunks:
        raise RuntimeError("No text data found to process.")

    embeddings = embed_text(all_chunks)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.stack(embeddings))

    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "w", encoding="utf-8") as f:
        for meta, text in zip(metadata, all_chunks):
            f.write(json.dumps({"meta": meta, "text": text}) + "\n")

    print(f"FAISS index and metadata saved in {VECTOR_DIR}")

if __name__ == "__main__":
    main()
