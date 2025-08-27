# Prompt Examples — Showing Your Thinking

This document contains representative prompts used during development, with reasoning for each. These examples illustrate structured AI-assisted problem-solving and intentional design choices.

1.1 Project prompt:You are a senior AI engineer and systems architect. You will design and implement a complete RAG-based app called “Personal Codex — Candidate Agent” entirely from scratch based on the project brief I provide. Think critically, minimize assumptions, and deliver runnable, high-quality code.

### 1.1 Prompt: Generate Chunking Logic
**Prompt:**  
"Write Python code to split a long text into ~400 token-ish chunks with a ~50 token overlap. Prefer sentence boundaries. Use nltk's sent_tokenize. Return a list of strings."

**Why used:**  
To quickly create a reliable chunking mechanism for text ingestion that preserves sentence boundaries and ensures context for embeddings.

### 2. Prompt: Improve Chunk Overlap Logic
**Prompt:**  
"Enhance chunking function to ensure 50-token overlap between segments for better context preservation across chunks."

**Why used:**  
To maintain semantic continuity between chunks and improve retrieval accuracy.


### 3. Prompt: Design Interview-mode System Prompt
**Prompt:**  
"Produce a system prompt that instructs an LLM to answer in first-person, professional, concise manner and to list technologies with years of experience if available."

**Why used:**  
To make Interview mode realistic for technical Q&A scenarios and job preparation simulations.

### 4. Prompt: Create Retrieval Function
**Prompt:**  
"Write a function retrieve(query, k) that loads FAISS index and returns top-k chunks with metadata for context injection."

**Why used:**  
To enable semantic search for user queries against stored document embeddings, forming the basis of RAG (Retrieval-Augmented Generation).


### 5. Prompt: Build Streamlit UI Layout
**Prompt:**  
"Create a Streamlit app with a two-column layout: left for controls (mode selector, upload button), right for Q&A interface."

**Why used:**  
To provide a clean and intuitive interface for interacting with the system.

### 6. Prompt: Add File Upload in Sidebar
**Prompt:**  
"Add a Streamlit sidebar file uploader to accept multiple files, save them to /data directory, and show confirmation message."

**Why used:**  
To allow easy addition of documents into the knowledge base from the user interface.


### 7. Prompt: Trigger Ingest Process from UI
**Prompt:**  
"Add a button in Streamlit that runs ingest.py when clicked and displays the log output in the app."

**Why used:**  
To let users refresh the knowledge base after uploading new documents without leaving the app.


### 8. Prompt: Display Supporting Chunks
**Prompt:**  
"After showing the answer, display top-k retrieved chunks with source filename and snippet text in a readable format."

**Why used:**  
To improve transparency and trust by showing where the answer was derived from.


### 9. Prompt: Add Deployment Instructions
**Prompt:**  
"Write deployment steps for Streamlit Cloud including how to set environment variables and handle API keys securely."

**Why used:**  
To ensure a straightforward path for demo and production deployment, following best practices for secret management.


### 10. Prompt: Draft Comprehensive README
**Prompt:**  
"Write a README for the Personal Codex project that explains the architecture, how to run ingest, how to deploy on Streamlit, and includes sample questions and 'future improvements' section."

**Why used:**  
To create a clear, structured README that helps others understand and use the project easily while demonstrating professional documentation standards.
