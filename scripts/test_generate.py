import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models_to_test = ["gemini-2.5-flash-lite", "gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-pro"]
for model_name in models_to_test:
    try:
        print(f"Testing {model_name}...", flush=True)
        resp = client.models.generate_content(
            model=model_name,
            contents="Say 'OK'",
        )
        print(f"-> SUCCESS with {model_name}: {resp.text.strip()}", flush=True)
        break
    except Exception as e:
        print(f"-> {model_name} failed: {e}", flush=True)
