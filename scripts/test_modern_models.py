import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

for m in ["gemini-3.5-flash-lite", "gemini-3.8-flash"]:
    try:
        print(f"Testing {m}...", flush=True)
        resp = client.models.generate_content(
            model=m,
            contents="Say 'OK'",
        )
        print(f"-> SUCCESS with {m}: {resp.text.strip()}", flush=True)
        break
    except Exception as e:
        print(f"-> {m} failed: {e}", flush=True)
