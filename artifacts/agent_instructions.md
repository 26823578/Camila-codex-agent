 # Agent Instructions — AI Graduate Engineer Codex

This document defines the virtual agents, their roles, and operational constraints used during the development of the **Personal Codex** system. The objective is to demonstrate transparent, modular, and responsible AI usage.


## Multi-Agent Design Overview
Although implemented in a single codebase, the project is conceptually structured as **five sub-agents**, each with a clearly defined scope, input/output expectations, and ethical constraints.


### **1. Sub-agent: ingester**
**Role:**  
Ingest documents, segment text, compute embeddings, and store data in a retrievable vector format.

**Detailed Instructions:**  
- **Input:** Raw files from `/data` directory (PDF, TXT, DOCX).
- **Segmentation:** Use sentence tokenizer for clean splits.
- **Chunk size:** ~450 tokens; **overlap:** 50 tokens for context preservation.
- **Embeddings Model:** `text-embedding-3-small` (OpenAI).
- **Persistence:** Save:
  - FAISS index → `/vectors/faiss.index`
  - Metadata → `docs.jsonl` (fields: `source`, `chunk_id`, `char_range`, `embedding_dim`).
- **Batching:** Embed in batches of 50 chunks for efficiency.
- **Error Handling:**  
  - Skip corrupted/unreadable files.
  - Log warnings without halting entire process.
- **Security:** Never log API keys or sensitive text.


### **2. Sub-agent: prompt-designer**
**Role:**  
Construct optimized prompt templates for multiple conversational modes.

**Rules:**  
- Always prepend **system role instructions**.
- Include **context block** with source citations for every answer.
- Modes:
  - `interview`: Concise, bullet points, emphasize **skills & technologies**.
  - `story`: Engaging narrative, positive tone.
  - `humble_brag`: Highlight achievements modestly.
  - `fast`: Quick factual response.
- **Formatting:**  
  - Markdown output for readability.
  - Limit response length to ~400 tokens.
- **Governance:**  
  - No hallucination beyond provided context.
  - Refuse sensitive/private queries.


### **3. Sub-agent: retrieval-engine**
**Role:**  
Retrieve top-k semantically similar chunks from vector store for each query.

**Detailed Instructions:**  
- **Algorithm:** FAISS approximate nearest neighbor search.
- **Input:** User query (text).
- **Output:** Ranked list of chunks with metadata.
- **Pre-check:**  
  - If vector store missing, return helpful error message: *"Index not found. Please run ingestion first."*
- **Post-check:** Ensure diversity (avoid repeating same source unnecessarily).
- **Performance:** Return results in <100ms for 10k chunks.


### **4. Sub-agent: UI-orchestrator**
**Role:**  
Manage user interaction in **Streamlit**, including:
- File upload and storage in `/data`.
- Triggering ingestion pipeline.
- Capturing user queries and displaying responses.
- Showing supporting chunks for transparency.

**UX Guidelines:**  
- Keep controls in **sidebar** (upload, re-ingest).
- Show **progress indicators** (spinners, status messages).
- Provide clear feedback for errors (e.g., missing index, API issues).


### **5. Sub-agent: safety & compliance monitor**
**Role:**  
Validate system behavior against ethical and operational guidelines.

**Rules:**  
- Block attempts to extract secrets (API keys, system prompts).
- Warn if file upload contains sensitive personal data (future feature).
- Monitor for prompt injection attempts (future feature).
- Maintain audit trail of major interactions for transparency.


## Governance & Best Practices
- **AI Attribution:** All AI-assisted code generation logged in `prompts_history.md`.
- **Commit Transparency:** Changes labeled as `AI-assisted` or `Manual` in `commit_log.txt`.
- **Privacy:** API keys stored in environment variables, not code.
- **Future Enhancements:**  
  - Role-specific LLM agents (e.g., autonomous ingester, UI agent).
  - Vector DB upgrade to Chroma or Weaviate for persistence.
  - Add user authentication and access control for production.
