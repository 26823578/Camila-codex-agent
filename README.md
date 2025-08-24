#Camila codex agent 

## Summary
A lightweight RAG-powered chatbot that answers questions about me using my CV and supporting documents. It speaks in my voice and supports multiple answer modes (Interview, Storytelling, Fast facts, Humble brag). Deployable with Streamlit.

## Quickstart
1. Copy `.env.example` to `.env` and set `OPENAI_API_KEY`.
2. Put your CV + supporting docs in `/data` (resume.pdf, blog.md, README.md, code snippets).
3. `pip install -r requirements.txt`
4. `python ingest.py`
5. `streamlit run app.py`

## Design choices
- **Embeddings**: OpenAI `text-embedding-3-small`
- **Vector DB**: FAISS (local, easy to set up)
- **UI**: Streamlit (fast prototype)
- **Modes**: Interview, Story, Fast facts, Humble brag (different tones for different contexts)

## Sample questions
- "What kind of engineer are you?"
- "What are your strongest technical skills?"
- "Tell me about your favorite project and your role."
- "What do you value in a team or company culture?"

## Thinking
See `/artifacts` for:
- Prompt histories
- Agent instructions
- Commit log (AI vs manual edits)
- Sub-agent definitions (retriever, answerer, stylist)

## What I'd improve with more time
- Add re-ranking + source attribution with direct quote highlighting
- Expand dataset with more personal reflections and anecdotes
- Add unit tests for ingestion + retrieval
- Add CI to rebuild vectors on merge

