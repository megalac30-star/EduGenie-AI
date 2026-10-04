import json
import re

from gemini_client import generate_text


def clean_json_block(text):

    text = text.strip()

    text = re.sub(
        r"^```(?:json)?\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"\s*```$",
        "",
        text
    )

    return text.strip()


def generate_quiz(passage):

    prompt = f"""
Create exactly THREE multiple-choice
questions from the following educational
passage.

Return ONLY valid JSON.

Required structure:

{{
    "questions": [
        {{
            "question": "Question",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": 0,
            "explanation": "Explanation"
        }}
    ]
}}

Rules:

1. Exactly 3 questions.
2. Exactly 4 options per question.
3. answer must be a zero-based index.
4. Questions must be based on the passage.
5. Distractors should be plausible.
6. No Markdown.
7. No text outside JSON.

Passage:

{passage}
"""

    raw = generate_text(
        prompt,
        temperature=0.2,
        json_mode=True
    )

    raw = clean_json_block(raw)

    try:

        data = json.loads(raw)

        if "questions" not in data:
            raise ValueError(
                "Missing questions field."
            )

        questions = data["questions"]

        if len(questions) != 3:
            raise ValueError(
                "Quiz must contain exactly 3 questions."
            )

        for question in questions:

            if not isinstance(
                question.get("question"),
                str
            ):
                raise ValueError(
                    "Invalid question."
                )

            options = question.get("options")

            if not isinstance(options, list):
                raise ValueError(
                    "Options must be a list."
                )

            if len(options) != 4:
                raise ValueError(
                    "Each question must have 4 options."
                )

            answer = question.get("answer")

            if answer not in range(4):
                raise ValueError(
                    "Invalid answer index."
                )

            if "explanation" not in question:
                question["explanation"] = ""

        return data

    except Exception as error:

        raise RuntimeError(
            f"Quiz generation failed: {error}"
        )