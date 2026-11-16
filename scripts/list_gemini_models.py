import os
import sys
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
print(f"API key loaded: length {len(api_key) if api_key else 0}", flush=True)

try:
    from google import genai
    client = genai.Client(api_key=api_key)
    print("Listing available models from Gemini API...", flush=True)
    count = 0
    for m in client.models.list():
        # Print model names that support generateContent
        supported = getattr(m, 'supported_generation_methods', []) or getattr(m, 'supported_actions', [])
        print(f"Model: {m.name}", flush=True)
        count += 1
        if count >= 10:
            break
    print(f"Total listed: {count}", flush=True)
except Exception as e:
    print(f"Error listing models: {type(e).__name__} - {e}", flush=True)
