import streamlit as st
from dotenv import load_dotenv
import os
from utils import retrieve
from prompts import construct_prompt
import openai
import subprocess

# Load environment variables
load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_COMPLETION_MODEL", "gpt-4o-mini")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit page setup
st.set_page_config(page_title="Personal Codex", layout="wide")
st.title("Personal Codex — Candidate Agent")

# Sidebar: Upload & Ingest Controls
with st.sidebar:
    st.header("Data Management")
    uploaded = st.file_uploader(
        "Upload your CV and supporting documents",
        accept_multiple_files=True,
        type=["pdf", "txt", "docx"]
    )
    if uploaded:
        os.makedirs("data", exist_ok=True)
        for f in uploaded:
            path = os.path.join("data", f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
        st.success(f"{len(uploaded)} file(s) saved to /data.")

    if st.button("Re-run ingest"):
        with st.spinner("Rebuilding FAISS index..."):
            proc = subprocess.run(
                ["python", "ingest.py"], capture_output=True, text=True
            )
            if proc.returncode == 0:
                st.success("Ingest finished successfully!")
            else:
                st.error("Ingest failed. See logs below:")
                st.subheader("Error Details")
                st.code(proc.stdout + "\n\n" + proc.stderr)

    st.markdown("---")
    st.header("Modes Explained")
    st.write("""
- **Interview**: Professional and concise, lists skills and experience.
- **Story**: Friendly, narrative-style answers.
- **Fast**: One-liner, direct answers.
- **Humble Brag**: Confident tone, highlighting achievements subtly.
    """)

    st.markdown("---")
    st.header("Sample Questions")
    st.write("- What kind of engineer are you?")
    st.write("- Summarize your experience in one paragraph.")
    st.write("- What programming languages do you know?")
    st.write("- Describe your proudest achievement.")

# Main layout: Q&A controls and results
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Controls")
    mode = st.selectbox("Mode", ["interview", "story", "fast", "humble_brag"], index=0)
    k = st.slider("Retrieval chunks (k)", 1, 8, 4)

with col2:
    st.header("Ask the Codex")
    q = st.text_input("Type your question:", placeholder="e.g., What kind of engineer are you?")
    
    if st.button("Ask") and q.strip():
        with st.spinner("Fetching the best answer..."):
            try:
                context_chunks = retrieve(q, k=k)
                if not context_chunks:
                    st.error("No context retrieved. Please upload and ingest your documents first.")
                else:
                    # Build the prompt and get mode info
                    prompt, mode_info = construct_prompt(mode, context_chunks, q)

                    # Call OpenAI API
                    resp = openai.ChatCompletion.create(
                        model=OPENAI_MODEL,
                        messages=[{"role": "system", "content": prompt}],
                        temperature=mode_info.get("temperature", 0.0),
                        max_tokens=400
                    )
                    answer = resp["choices"][0]["message"]["content"].strip()

                    st.success("Answer Ready!")
                    st.subheader("Answer")
                    st.write(answer)

                    # Expandable context
                    with st.expander("See supporting context"):
                        for i, c in enumerate(context_chunks):
                            st.markdown(f"**{i+1}. Source:** `{c['meta']['source']}` (chunk {c['meta']['chunk']})")
                            st.write(c['text'][:800] + ("..." if len(c['text']) > 800 else ""))

            except Exception as e:
                st.error(f"Error processing your request: {e}")
