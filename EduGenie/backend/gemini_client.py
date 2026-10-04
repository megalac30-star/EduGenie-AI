import os
import time
import random
from functools import lru_cache

from google import genai
from google.genai import types


# ============================================================
# GEMINI CLIENT
# ============================================================

@lru_cache(maxsize=1)
def get_client():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=api_key)


# ============================================================
# CHECK TRANSIENT ERROR
# ============================================================

def is_retryable_error(error):

    error_text = str(error).lower()

    retry_codes = [
        "429",
        "500",
        "502",
        "503",
        "504",
        "unavailable",
        "overloaded",
        "temporarily"
    ]

    return any(code in error_text for code in retry_codes)


# ============================================================
# GENERATE TEXT
# ============================================================

def generate_text(
    prompt: str,
    temperature: float = 0.4,
    json_mode: bool = False
):

    client = get_client()

    # Primary model
    primary_model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash"
    )

    # Fallback model
    fallback_model = "gemini-2.5-flash-lite"

    models = [primary_model]

    if fallback_model != primary_model:
        models.append(fallback_model)

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=2500
    )

    if json_mode:
        config.response_mime_type = "application/json"

    last_error = None

    # ========================================================
    # TRY PRIMARY + FALLBACK MODEL
    # ========================================================

    for model in models:

        for attempt in range(4):

            try:

                print(
                    f"Gemini request | model={model} | "
                    f"attempt={attempt + 1}"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=config
                )

                text = getattr(
                    response,
                    "text",
                    None
                )

                if not text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                print(
                    f"Gemini response received | model={model}"
                )

                return text.strip()

            except Exception as error:

                last_error = error

                print(
                    f"Gemini error | model={model} | "
                    f"attempt={attempt + 1}: {error}"
                )

                # Retry only temporary errors
                if not is_retryable_error(error):
                    raise

                # Exponential backoff
                if attempt < 3:

                    delay = (2 ** attempt) + random.uniform(0, 1)

                    print(
                        f"Retrying in {delay:.1f} seconds..."
                    )

                    time.sleep(delay)

        print(
            f"Primary attempts failed. "
            f"Trying next model: {fallback_model}"
        )

    # ========================================================
    # ALL MODELS FAILED
    # ========================================================

    raise RuntimeError(
        "Gemini service is temporarily unavailable. "
        "Both Gemini models failed after retries. "
        f"Last error: {last_error}"
    )