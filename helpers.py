# helpers.py
import os
import streamlit as st

def get_api_key():
    """
    Returns OpenAI API key from either environment (.env) or Streamlit secrets (cloud).
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key and "OPENAI_API_KEY" in st.secrets:
        key = st.secrets["OPENAI_API_KEY"]
    return key
