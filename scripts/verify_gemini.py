import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load backend/.env
env_path = Path(__file__).resolve().parent.parent / "backend" / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("ERROR: GEMINI_API_KEY not found in backend/.env")
    sys.exit(1)

# Check presence without printing
print("SUCCESS: GEMINI_API_KEY detected in environment (length: {})".format(len(api_key)))

try:
    from google import genai
    from google.genai import types

    # Note: official google-genai client
    client = genai.Client(api_key=api_key)
    
    # Test models: modern free tier
    test_models = ["gemini-3.8-flash", "gemini-2.0-flash", "gemini-2.5-flash"]
    connected = False
    
    for model_name in test_models:
        try:
            print(f"Testing model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents="Ping. Respond with 'PONG' and nothing else.",
            )
            print(f"SUCCESS: Received response from {model_name}: {response.text.strip()}")
            connected = True
            break
        except Exception as e:
            print(f"Note: {model_name} test returned: {type(e).__name__} - {e}")
            
    if connected:
        print("GEMINI CONNECTIVITY VERIFIED: Official google-genai SDK operational on free tier.")
        sys.exit(0)
    else:
        print("FAILED: Could not establish response from tested models.")
        sys.exit(1)

except Exception as err:
    print(f"ERROR initializing or calling google-genai: {type(err).__name__} - {err}")
    sys.exit(1)
