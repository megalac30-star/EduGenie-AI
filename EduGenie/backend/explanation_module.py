from gemini_client import generate_text


def explain_topic(topic):

    prompt = f"""
You are EduGenie,
a beginner-friendly educational teacher.

Explain this topic:

{topic}

Use the following structure:

1. Simple definition
2. How it works
3. Easy example
4. Key points to remember

Use simple language.

Assume that the learner has little
or no previous knowledge.

Make the explanation clear and educational.
"""

    return generate_text(
        prompt,
        temperature=0.35
    )