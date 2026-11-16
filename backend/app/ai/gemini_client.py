import logging
from typing import Optional
from google import genai
from google.genai import types
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiAIClient:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL
        self._client: Optional[genai.Client] = None

        if self.api_key:
            try:
                self._client = genai.Client(api_key=self.api_key)
                logger.info(f"Gemini client initialized with model {self.model_name}")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {e}")
                self._client = None
        else:
            logger.warning("No GEMINI_API_KEY configured.")

    @property
    def is_available(self) -> bool:
        return self._client is not None

    async def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> Optional[str]:
        if not self._client:
            return None

        try:
            config = types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1000,
            )
            if system_instruction:
                config.system_instruction = system_instruction

            response = self._client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=config,
            )
            if response and response.text:
                return response.text.strip()
            return None
        except Exception as e:
            logger.error(f"Gemini API generation error: {e}")
            return None


gemini_client = GeminiAIClient()
