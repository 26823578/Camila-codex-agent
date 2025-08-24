# Prompts History — AI Graduate Engineer Project

This file documents interactions with AI coding assistants (e.g., ChatGPT, Copilot) during project development.  
Each entry includes: **Prompt**, **AI Response summary**, **Manual Edits**, and **Commit message**.

---

### Prompt 1 → Create `ingest.py` for FAISS
**Prompt:**  
"Write a Python script to ingest PDF and text files, chunk by sentences, embed using OpenAI embeddings, and store FAISS index."

**AI Response:**  
- Generated script using PyPDF2 and FAISS.
- Used `text-embedding-ada-002`.

**Manual edits:**  
- Changed model to `text-embedding-3-small`.
- Added overlap logic.
- Added JSONL metadata output.

**Commit:**  
`2025-08-21 10:05 - feat: add ingest.py (AI-assisted, manually enhanced)`

---

### Prompt 2 → Improve chunking method
**Prompt:**  
"Add overlapping chunks (50 tokens) and token counting with tiktoken to ingest.py."

**AI Response:**  
- Added overlap logic and token-based splitting.

**Manual edits:**  
- Fixed bug in token count for last chunk.
- Increased overlap from 30 to 50 tokens.

**Commit:**  
`2025-08-21 10:30 - refactor: improved chunking and overlap handling`

---

### Prompt 3 → Create `utils.py` retrieval function
**Prompt:**  
"Write a function `retrieve(query, k)` that loads FAISS index and returns top-k chunks with metadata."

**AI Response:**  
- Implemented FAISS search and returned scores.

**Manual edits:**  
- Added metadata from docs.jsonl.
- Handled missing index with custom error.

**Commit:**  
`2025-08-21 11:00 - feat: retrieval utility for FAISS`

---

### Prompt 4 → Build Streamlit UI skeleton
**Prompt:**  
"Create a Streamlit app with two columns: left for controls, right for query input and answers."

**AI Response:**  
- Generated a simple layout with columns.

**Manual edits:**  
- Styled UI with headers.
- Added spinner during retrieval.

**Commit:**  
`2025-08-21 12:15 - feat: initial Streamlit UI structure`

---

### Prompt 5 → Add mode switcher to UI
**Prompt:**  
"Add a dropdown to select modes: interview, story, fast, humble_brag."

**AI Response:**  
- Implemented selectbox and passed mode to prompt constructor.

**Manual edits:**  
- Styled sidebar controls.
- Added info about each mode in README.

**Commit:**  
`2025-08-21 12:45 - feat: added mode switcher to UI`

---

### Prompt 6 → Create `prompts.py` with dynamic templates
**Prompt:**  
"Write a function construct_prompt(mode, context_chunks, question) with templates for each mode."

**AI Response:**  
- Created four templates with placeholders.

**Manual edits:**  
- Added explicit context block with sources.
- Added markdown formatting for answers.

**Commit:**  
`2025-08-21 13:10 - feat: prompt templates for all modes`

---

### Prompt 7 → Improve UI with sidebar upload
**Prompt:**  
"Add sidebar file uploader to Streamlit and save files to /data folder."

**AI Response:**  
- Added `st.file_uploader()`.

**Manual edits:**  
- Added success message after save.
- Added ingest trigger button.

**Commit:**  
`2025-08-21 14:00 - feat: sidebar upload and ingestion trigger`

---

### Prompt 8 → Add FAISS rebuild on upload
**Prompt:**  
"When new files uploaded, provide a button to rebuild FAISS index."

**AI Response:**  
- Suggested subprocess call for ingest.py.

**Manual edits:**  
- Added spinner and error handling for ingestion.

**Commit:**  
`2025-08-21 14:30 - feat: rebuild FAISS from UI`

---

### Prompt 9 → Display supporting chunks
**Prompt:**  
"After showing the answer, display top-k supporting chunks with source and snippet."

**AI Response:**  
- Created markdown for sources.

**Manual edits:**  
- Limited snippet length to 800 chars.
- Highlighted chunk number.

**Commit:**  
`2025-08-21 15:00 - feat: show supporting chunks`

---

### Prompt 10 → Add OpenAI API integration
**Prompt:**  
"Integrate OpenAI ChatCompletion with the constructed prompt."

**AI Response:**  
- Wrote function with GPT-3.5 default.

**Manual edits:**  
- Changed to `OPENAI_MODEL` env variable.
- Used `gpt-4o-mini` for better quality.

**Commit:**  
`2025-08-21 15:30 - feat: integrated OpenAI API with dynamic prompts`

---

### Prompt 11 → Write .env loader
**Prompt:**  
"Add dotenv support to load OPENAI_API_KEY."

**AI Response:**  
- Added `load_dotenv()`.

**Manual edits:**  
- Added fallback model if not set.
- Updated README.

**Commit:**  
`2025-08-21 16:00 - feat: dotenv support for API key`

---

### Prompt 12 → Add error handling for API failures
**Prompt:**  
"Show an error message in Streamlit if OpenAI API call fails."

**AI Response:**  
- Added try/except with `st.error()`.

**Manual edits:**  
- Logged full error details in code block.

**Commit:**  
`2025-08-21 16:30 - fix: API error handling`

---

### Prompt 13 → Optimize ingestion for large files
**Prompt:**  
"Use batch embedding calls for efficiency during ingestion."

**AI Response:**  
- Added loop batching of 100 chunks.

**Manual edits:**  
- Reduced batch size to 50 for stability.

**Commit:**  
`2025-08-21 17:00 - perf: batch embeddings in ingestion`

---

### Prompt 14 → Add README deployment steps
**Prompt:**  
"Write deployment instructions for Streamlit Cloud."

**AI Response:**  
- Wrote steps for Streamlit Cloud.

**Manual edits:**  
- Added secret management and repo link format.

**Commit:**  
`2025-08-21 17:30 - docs: added Streamlit Cloud deployment guide`

---

### Prompt 15 → Create agent_instructions.md
**Prompt:**  
"Write detailed roles and rules for sub-agents in multi-agent design."

**AI Response:**  
- Suggested basic roles for ingester and prompt-designer.

**Manual edits:**  
- Expanded to 5 agents, added governance section.

**Commit:**  
`2025-08-21 18:00 - docs: added agent_instructions.md`

---

### Prompt 16 → Create commit log template
**Prompt:**  
"Give me a sample commit_log.txt format for transparency."

**AI Response:**  
- Provided timestamp + message format.

**Manual edits:**  
- Added tags like `AI-assisted`, `manual`.

**Commit:**  
`2025-08-21 18:15 - docs: added commit log template`

---

### Prompt 17 → Improve UI aesthetics
**Prompt:**  
"Add spacing, headers, and better layout to Streamlit app."

**AI Response:**  
- Suggested using columns and headers.

**Manual edits:**  
- Added `st.set_page_config(layout="wide")` and reorganized.

**Commit:**  
`2025-08-21 18:45 - style: improved Streamlit UI`

---

### Prompt 18 → Add mode descriptions in UI
**Prompt:**  
"Show tooltips or help text for each mode."

**AI Response:**  
- Added short descriptions in README.

**Manual edits:**  
- Implemented `st.info()` for mode hints.

**Commit:**  
`2025-08-21 19:10 - feat: added mode info tooltips`

---

### Prompt 19 → Validate empty input
**Prompt:**  
"Prevent asking if question field is empty."

**AI Response:**  
- Added `if q.strip()` check.

**Manual edits:**  
- Added error message for blank input.

**Commit:**  
`2025-08-21 19:30 - fix: handle empty input gracefully`

---

### Prompt 20 → Prepare artifacts directory
**Prompt:**  
"List final artifacts required: README, prompts history, agent instructions, commit log."

**AI Response:**  
- Provided list and structure.

**Manual edits:**  
- Created folders and linked in sidebar.

**Commit:**  
`2025-08-21 20:00 - chore: prepared artifacts directory`
