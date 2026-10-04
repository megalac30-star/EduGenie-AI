from gemini_client import generate_text


def get_learning_recommendations(topic):

    prompt = f"""
You are EduGenie,
a personalized learning advisor.

Create a structured learning path
for the following topic:

{topic}

Organize the plan as:

1. Prerequisites
2. Beginner level
3. Intermediate level
4. Advanced level
5. Suggested timeline
6. Practice projects
7. Recommended resource types
8. Weekly study routine
9. Final project

The learning path should be practical
and suitable for a student.

Progress should move gradually
from beginner to advanced.

Do not invent specific URLs.

Use clear headings and bullet points.
"""

    return generate_text(
        prompt,
        temperature=0.45
    )