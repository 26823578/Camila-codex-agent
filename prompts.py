# Reasoning: prompts.py centralises all prompt templates for easy maintenance 
# and mode-specific customisation. System prompt sets the agent's voice and 
# mode behavior. User prompt injects retrieved chunks and question. This allows
# creative prompt strategies as per bonus. Modes are defined to match brief: 
# interview (professional), story (narrative), fast (bullets), humble_brag (confident).

def construct_prompt(mode, context_chunks, question):
    """
    Builds a system prompt for the LLM based on the selected mode.
    Includes retrieved context for grounding answers.
    """

    # Combine all context into one string
    context_text = "\n\n".join(
        [f"Source: {c['meta']['source']} | Chunk: {c['meta']['chunk']}\n{c['text']}" for c in context_chunks]
    )

    # Mode-specific instructions
    if mode == "interview":
        system_prompt = f"""
You are acting as the candidate in a job interview. Answer in FIRST-PERSON, professional, and concise.
If asked about skills or technologies, list them clearly (e.g., "I have 3 years of experience in Python, 2 years in SQL").
Base answers ONLY on the context provided. Do NOT invent details not in the context.

Context:
{context_text}

Question:
{question}
"""
        mode_info = {"temperature": 0.3}

    elif mode == "story":
        system_prompt = f"""
You are writing a short story or narrative answer about yourself, using a friendly tone.
Use the provided context as inspiration for the details. Be engaging but truthful.

Context:
{context_text}

Question:
{question}
"""
        mode_info = {"temperature": 0.7}

    elif mode == "fast":
        system_prompt = f"""
Answer the question in ONE OR TWO sentences maximum, using a direct tone.
Stick strictly to the context provided.

Context:
{context_text}

Question:
{question}
"""
        mode_info = {"temperature": 0.2}

    elif mode == "humble_brag":
        system_prompt = f"""
Answer in a confident and professional tone that subtly highlights achievements without sounding arrogant.
Base your response on the context only.

Context:
{context_text}

Question:
{question}
"""
        mode_info = {"temperature": 0.5}

    else:
        raise ValueError(f"Unknown mode: {mode}")

    return system_prompt.strip(), mode_info
