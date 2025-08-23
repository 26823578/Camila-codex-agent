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

# Left column: controls
col1, col2 = st.columns([1,3])

with col1:
    st.header("Controls")
    mode = st.selectbox("Mode", ["interview","story","fast","humble_brag"], index=0)
    k = st.slider("Retrieval chunks (k)", 1, 8, 4)
    st.write("Upload files to /data to update the knowledge base.")
    if st.button("Re-run ingest (reads ./data)"):
        st.info("Running ingest.py...")
        # run ingest script (assuming ingest.py is present)
        proc = subprocess.run(["python","ingest.py"], capture_output=True, text=True)
        st.code(proc.stdout + "\n\n" + proc.stderr)
        st.success("Ingest finished.")

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
            st.write(c['text'][:800] + ("..." if len(c['text'])>800 else ""))

st.sidebar.header("Project links")
st.sidebar.markdown("- README\n- artifacts/\n")
