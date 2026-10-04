from gemini_client import generate_text


def summarize_text(text):

    prompt = f"""
You are EduGenie,
an educational summarization assistant.

Summarize the following educational
content for quick revision.

Requirements:

- Keep the important information.
- Remove unnecessary repetition.
- Use simple language.
- Do not add information.
- Keep the original meaning.
- Provide important points as bullets.
- Make the summary easy for a student to revise.

Educational text:

{text}
"""

    return generate_text(
        prompt,
        temperature=0.25
    )