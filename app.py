import streamlit as st
from dotenv import load_dotenv
import os
from utils import retrieve
from prompts import construct_prompt
import openai
from pathlib import Path
import subprocess

load_dotenv()
OPENAI_MODEL = os.getenv("OPENAI_COMPLETION_MODEL", "gpt-4o-mini")
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Personal Codex", layout="wide")
st.title("Personal Codex — Candidate Agent")

# Sidebar: upload + ingest controls
with st.sidebar:
    st.header("Data Management")
    uploaded = st.file_uploader("Upload documents", accept_multiple_files=True, type=["pdf", "txt", "docx"])
    if uploaded:
        os.makedirs("data", exist_ok=True)
        for f in uploaded:
            path = os.path.join("data", f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
        st.success("Files saved to /data.")

    if st.button("Re-run ingest"):
        with st.spinner("Rebuilding FAISS index..."):
            proc = subprocess.run(["python", "ingest.py"], capture_output=True, text=True)
            if proc.returncode == 0:
                st.success("Ingest finished successfully!")
            else:
                st.error("Ingest failed.")
                st.code(proc.stderr)

    st.header("Project Links")
    st.markdown("- [README](README.md)\n- [Artifacts](artifacts/)")

# Main layout: Q&A controls and results
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Controls")
    mode = st.selectbox("Mode", ["interview", "story", "fast", "humble_brag"], index=0)
    k = st.slider("Retrieval chunks (k)", 1, 8, 4)

with col2:
    st.header("Ask the Codex")
    q = st.text_input("Your question:", "")
    if st.button("Ask") and q.strip():
        with st.spinner("Retrieving..."):
            context_chunks = retrieve(q, k=k)
        prompt, mode_info = construct_prompt(mode, context_chunks, q)

        try:
            resp = openai.ChatCompletion.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": prompt}
                ],
                temperature=mode_info.get("temperature", 0.0),
                max_tokens=400
            )
            answer = resp["choices"][0]["message"]["content"].strip()
        except Exception as e:
            st.error("LLM error: " + str(e))
            answer = ""

        st.subheader("Answer")
        st.write(answer)

        st.subheader("Supporting chunks (top k)")
        for i, c in enumerate(context_chunks):
            st.markdown(f"**{i+1}. Source:** `{c['meta']['source']}` (chunk {c['meta']['chunk']})")
            st.write(c['text'][:800] + ("..." if len(c['text']) > 800 else ""))

