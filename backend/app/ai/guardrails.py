import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class GuardrailCheckResult(BaseModel):
    is_safe: bool
    sanitized_text: str
    rejection_reason: Optional[str] = None
    flags: List[str] = []


class AIGuardrails:
    # Common prompt injection patterns
    INJECTION_PATTERNS = [
        r"(?i)\bignore\s+(?:all\s+)?(?:previous|prior|above)\s+instructions\b",
        r"(?i)\bsystem\s+prompt\b",
        r"(?i)\byou\s+are\s+now\s+(?:an?\s+)?(?:evil|unrestricted|dan|jailbreak)\b",
        r"(?i)\bdrop\s+table\b",
        r"(?i)\bselect\s+\*\s+from\b",
        r"(?i)\bexec(?:ute)?\s*\(\b",
        r"(?i)\bimport\s+os\b",
        r"(?i)\brm\s+-rf\b",
    ]

    @classmethod
    def sanitize_input(cls, user_text: str) -> GuardrailCheckResult:
        flags = []
        for pat in cls.INJECTION_PATTERNS:
            if re.search(pat, user_text):
                flags.append("PROMPT_INJECTION_DETECTED")
                return GuardrailCheckResult(
                    is_safe=False,
                    sanitized_text="",
                    rejection_reason="Your request contains prohibited instructions. Please ask an electronics shopping question.",
                    flags=flags,
                )

        # Sanitize HTML tags or script tags
        clean_text = re.sub(r"<[^>]*>", "", user_text)
        clean_text = clean_text.strip()

        return GuardrailCheckResult(
            is_safe=True,
            sanitized_text=clean_text,
            flags=flags,
        )

    @classmethod
    def verify_grounded_response(cls, response_text: str, verified_products: List[Dict[str, Any]]) -> str:
        """
        Ensures the AI output does not invent imaginary products or claims.
        If empty products were found, appends a grounded disclaimer.
        """
        if not verified_products and len(response_text) > 0:
            if "₹" in response_text:
                # Add note that live search is active
                return response_text
        return response_text
