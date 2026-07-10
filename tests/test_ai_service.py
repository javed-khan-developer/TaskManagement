from unittest.mock import MagicMock

import httpx
from openai import RateLimitError

from services.ai.gemini_service import AiService


def test_chat_returns_fallback_on_rate_limit():
    service = AiService.__new__(AiService)
    service.client = MagicMock()
    response = httpx.Response(
        429,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
    )
    service.client.chat.completions.create.side_effect = RateLimitError(
        message="You exceeded your current quota",
        response=response,
        body={"error": {"message": "quota"}},
    )

    reply = service.chat("hello")

    assert "temporarily unavailable" in reply.lower()
