# Prompts History — Personal Codex Project

This file documents interactions with AI coding assistants (ChatGPT, Claude, Grok) during project development.  
Each entry includes: **AI Tool Used**, **Prompt**, **AI Response summary**, **Manual Edits**, and **Commit message**.

---

### Initial Project Prompt → Full System Architecture
**AI Tool:** ChatGPT, Claude, Grok (Asked all tools, compared output snd combined ideas, using the best solution for each approach)
**Prompt:**  
"You are a senior AI engineer and systems architect. You will design and implement a complete RAG-based app called 'Personal Codex — Candidate Agent' entirely from scratch based on the project brief I provide. Think critically, minimize assumptions, and deliver runnable, high-quality code."

**AI Response:**  
- Generated complete project structure with RAG pipeline
- Created ingest.py, app.py, utils.py, and prompts.py
- Suggested FAISS for vector storage and Streamlit for UI
- Provided requirements.txt and basic README structure

**Manual edits:**  
- Updated OpenAI API calls to use newer client pattern
- Modified chunking strategy for better sentence boundaries
- Added multiple conversation modes (interview, story, fast, humble_brag)
- Enhanced error handling throughout

**Commit:**   - Initial commit with full RAG architecture`

---

### Prompt 1 → Create `ingest.py` for Document Processing
**AI Tool:** Claude  
**Prompt:**  
"Improve the document ingestion pipeline. Use sentence tokenisation instead of fixed chunks, add overlap between chunks, and ensure robust PDF/DOCX/TXT parsing."

**AI Response:**  
- Implemented NLTK sentence tokenisation
- Added 50-token overlap between chunks
- Created robust file type detection and parsing

**Manual edits:**  
- Switched from `text-embedding-ada-002` to `text-embedding-3-small`
- Added progress indicators during ingestion
- Enhanced metadata structure with chunk IDs

**Commit:**  
- created project files`

---

### Prompt 2 → Modular Retrieval System
**AI Tool:** Grok  
**Prompt:**  
"Create a separate utils.py module for retrieval logic. Keep it isolated from the main app for better modularity and testing."

**AI Response:**  
- Designed clean retrieval interface
- Implemented FAISS index loading and query processing
- Added error handling for missing indices

**Manual edits:**  
- Added metadata retrieval from JSONL files
- Improved error messages for better UX
- Added query embedding caching considerations

**Commit:**  
- Ingest.py updated, designed for simplicity and robustness`

---

### Prompt 3 → Multi-Mode Conversation System
**AI Tool:** ChatGPT  
**Prompt:**  
"Design a prompt system that can switch between different conversation modes: professional interview style, narrative storytelling, quick facts, and confident self-promotion."

**AI Response:**  
- Created mode-specific prompt templates
- Implemented temperature controls for each mode
- Added context injection with source attribution

**Manual edits:**  
- Fine-tuned prompt language for authenticity
- Added explicit first-person instructions for interview mode
- Enhanced context formatting with source metadata

**Commit:**  
- added separate mode definitions`

---

### Prompt 4 → Streamlit UI Development
**AI Tool:** Claude  
**Prompt:**  
"Build a clean Streamlit interface with file upload, mode selection, and real-time document ingestion. Make it user-friendly for non-technical users."

**AI Response:**  
- Created two-column layout with controls and Q&A sections
- Added sidebar for data management
- Implemented file upload with progress feedback

**Manual edits:**  
- Added mode explanations and sample questions
- Enhanced visual hierarchy with better headers
- Added expandable context display for transparency

**Commit:**  
 - Separate controls and Q&A into columns`

---

### Prompt 5 → Dynamic Document Upload
**AI Tool:** Grok  
**Prompt:**  
"Add functionality to upload new documents through the UI and trigger re-ingestion without redeploying the app."

**AI Response:**  
- Implemented multi-file upload widget
- Added subprocess call to run ingest.py
- Created progress indicators and error handling

**Manual edits:**  
- Added file validation and size limits
- Enhanced error reporting with detailed logs
- Improved success/failure feedback messages

**Commit:**  
- added self-reflection feature`

### Prompt 6 → Advanced RAG with Context Display
**AI Tool:** ChatGPT  
**Prompt:**  
"Enhance the RAG system to show supporting context chunks with source attribution. Make the system transparent so users can verify answers."

**AI Response:**  
- Added expandable context sections
- Implemented source metadata display
- Created chunk preview with character limits

**Manual edits:**  
- Limited chunk previews to 800 characters
- Added chunk numbering for easy reference
- Enhanced markdown formatting for readability

**Commit:**  
`- added sidebar file upload and ingest workflow`

---

### Prompt 7 → API Integration and Error Handling
**AI Tool:** Claude  
**Prompt:**  
"Integrate OpenAI's ChatCompletion API with proper error handling, rate limiting considerations, and environment variable management."

**AI Response:**  
- Implemented secure API key management
- Added comprehensive try-catch blocks
- Created user-friendly error messages

**Manual edits:**  
- Updated to use gpt-4o-mini for better performance
- Added fallback model configuration
- Enhanced error logging for debugging

**Commit:**  
- Added Dev Container Folder`

---

### Prompt 8 → Conversation Mode Refinement
**AI Tool:** Grok  
**Prompt:**  
"Refine the conversation modes to feel more natural and authentic. Each mode should have distinct personality while remaining grounded in the source documents."

**AI Response:**  
- Adjusted temperature settings per mode
- Enhanced prompt instructions for personality
- Added mode-specific response formatting

**Manual edits:**  
- Fine-tuned humble_brag mode to avoid arrogance
- Enhanced story mode for better narrative flow
- Optimised fast mode for conciseness

**Commit:**  
- created prompt examples with reasoning`

---

### Prompt 9 → OpenAI API Migration
**AI Tool:** ChatGPT  
**Prompt:**  
"Update the codebase to use the appropriate OpenAI Python client with the new API patterns. Ensure compatibility and fix any deprecation warnings."

**AI Response:**  
- Updated to openai.OpenAI() client pattern
- Changed embedding creation method
- Fixed response object access patterns

**Manual edits:**  
- Applied changes consistently across all files
- Added proper client initialization
- Updated error handling for new API responses

**Commit:**  
`- Use openai.OpenAI() to create a client`

---

### Prompt 10 → UI Polish and User Experience
**AI Tool:** Claude  
**Prompt:**  
"Polish the Streamlit interface with better spacing, clearer instructions, and helpful tooltips. Make it feel professional and intuitive."

**AI Response:**  
- Added mode explanations in sidebar
- Created sample questions section
- Improved visual hierarchy and spacing

**Manual edits:**  
- Customised page title and layout
- Added helpful placeholder text
- Enhanced progress indicators and feedback

**Commit:**  
- Streamlit UI improvements, better error handling`

---

### Prompt 11 → Documentation and Transparency
**AI Tool:** Grok  
**Prompt:**  
"Review repository documents as submitted. Create comprehensive documentation showing the AI-assisted development process, including agent instructions, commit logs, and prompt history."

**AI Response:**  
- Generated agent_instructions.md template
- Created commit log format
- Suggested prompt history structure

**Manual edits:**  
- Expanded to 5 conceptual sub-agents
- Added governance and best practices sections
- Enhanced transparency with detailed AI attribution

**Commit:**  
`- agent details`

---

### Prompt 12 → Final Integration and Testing
**AI Tool:** ChatGPT  
**Prompt:**  
"Review the entire codebase for consistency, fix any remaining API issues, and ensure all components work together seamlessly."

**AI Response:**  
- Identified API inconsistencies across files
- Suggested testing procedures
- Recommended deployment preparations

**Manual edits:**  
- Fixed remaining deprecated API calls
- Added comprehensive error handling
- Prepared final documentation

**Commit:**  
` - UI testing`

##Infamous Final Prompt: 
You are an AI engineer, use your technical skills to solve this issue through examining the code -- this prompt included app.py, ingest.py, utils.py -- outcome included solutions to the open.AI embedding issue, after examining the code, I made slight changes to ensure it matched the agent. This was acheived after various attempts. 

## AI Collaboration Summary

**Tools Used:**
- **ChatGPT**: Primary system architecture, API integration, final code review
- **Claude**: Document processing, UI development, documentation creation
- **Grok**: Modular design, error handling, transparency features

**Development Approach:**
- Started with high-level system prompt for full architecture
- Iteratively refined components with different AI assistants
- Combined AI suggestions with manual refinements for authenticity
- Maintained transparency through detailed commit tracking

**AI vs Manual Split:**
- **AI-Generated (~70%)**: Core architecture, API integrations, UI structure, documentation templates
- **Manual Edits (~30%)**: API updates, prompt fine-tuning, error handling, personality adjustments, transparency enhancements
