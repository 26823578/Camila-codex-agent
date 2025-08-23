BASE_INSTRUCTIONS = """You are the personal codex of the candidate. Use the provided context to answer precisely and honestly. If the answer is not found directly, say so and offer a reasonable, transparent inference or ask to see more documents."""

MODES = {
    "interview": {
        "system": "Answer in a concise, professional style suitable for a technical interview. Keep answers to 2-4 sentences. When listing skills, be specific (languages, frameworks, years).",
        "temperature": 0.0
    },
    "story": {
        "system": "Answer in a narrative, first-person voice. Provide short anecdotes and be reflective; 4-6 sentences.",
        "temperature": 0.7
    },
    "fast": {
        "system": "Answer in bullet points. Each bullet is a quick fact or short sentence. Keep it short.",
        "temperature": 0.0
    },
    "humble_brag": {
        "system": "Answer confidently and highlight achievements while remaining grounded. Use short examples and quantify impact when possible.",
        "temperature": 0.3
    }
}

def construct_prompt(mode_key: str, context_chunks: list, user_question: str):
    mode = MODES.get(mode_key, MODES["interview"])
    system = BASE_INSTRUCTIONS + "\n\n" + mode["system"]
    # include source metadata
    context_texts = []
    for c in context_chunks:
        src = c.get("meta", {}).get("source", "unknown")
        chunk_id = c.get("meta", {}).get("chunk", 0)
        context_texts.append(f"[source: {src} | chunk:{chunk_id}]\n{c['text']}")
    context = "\n\n---\n\n".join(context_texts)
    prompt = f"{system}\n\nContext:\n{context}\n\nUser: {user_question}\n\nAnswer:"
    return prompt, mode
