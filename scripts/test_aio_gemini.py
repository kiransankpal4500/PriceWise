import asyncio
from app.core.config import settings
from google import genai
from google.genai import types

async def test():
    c = genai.Client(api_key=settings.GEMINI_API_KEY)
    resp = await c.aio.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents="Say 'AI is working perfectly'",
    )
    print("AIO RESPONSE:", resp.text.strip())

if __name__ == "__main__":
    asyncio.run(test())
