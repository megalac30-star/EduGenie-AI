from gemini_client import generate_text


def answer_question(question: str):

    prompt = f"""
You are EduGenie, an intelligent educational
question-answering assistant.

Answer the student's question accurately
and clearly.

Student question:
{question}

Instructions:

1. Give the direct answer first.
2. Explain the answer simply.
3. Use examples when useful.
4. Use bullet points when appropriate.
5. Avoid unnecessary technical language.
6. Do not invent information.
7. Make the answer suitable for students.
8. Keep the answer reasonably concise.
"""

    return generate_text(
        prompt,
        temperature=0.3
    )