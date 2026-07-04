import os
import time

import streamlit as st


def get_api_key(user_api_key: str | None = None) -> str | None:
    if user_api_key:
        return user_api_key.strip()

    try:
        secret_key = st.secrets.get("GEMINI_API_KEY")
        if secret_key:
            return str(secret_key).strip()
    except Exception:
        pass

    env_key = os.getenv("GEMINI_API_KEY")
    return env_key.strip() if env_key else None


def get_gemini_client(api_key: str):
    try:
        from google import genai
    except ImportError as exc:
        raise RuntimeError("Missing google-genai. Install it with: pip install google-genai") from exc

    return genai.Client(api_key=api_key)


def generate_with_gemini(
    client,
    model_name: str,
    prompt: str,
    temperature: float,
    max_output_tokens: int,
) -> tuple[str, float]:
    try:
        from google.genai import types
    except ImportError as exc:
        raise RuntimeError("Missing google-genai. Install it with: pip install google-genai") from exc

    start = time.time()
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        ),
    )

    text = getattr(response, "text", None) or (
        "No text response returned by the model. "
        "Try lowering safety-sensitive content or changing the prompt."
    )
    return text.strip(), time.time() - start
