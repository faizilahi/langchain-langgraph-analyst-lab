"""Optional real LLM hook — disabled unless ENABLE_LIVE_LLM=1 and API key present."""
import os


def generate(prompt: str) -> str:
    if os.getenv("ENABLE_LIVE_LLM") != "1":
        raise RuntimeError("Live LLM disabled — teaching sim uses templates only.")
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("No OPENAI_API_KEY — simulation mode only.")
    return f"[stub would call LLM with prompt length {len(prompt)}]"
