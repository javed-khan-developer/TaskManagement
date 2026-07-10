from google import genai
from core.config import settings


class AiService:

    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.messages = []

    def chat(self, messages: list):
        if not settings.GEMINI_API_KEY:
            return "Gemini API key is not configured."

        prompt_text = "\n".join(
            f"{msg['role']}: {msg['parts'][0]['text']}" for msg in messages
        )

        self.messages.append(
            {
                "role": "user",
                "parts": [{"text": prompt_text}],
            }
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.messages,
        )

        ai_reply = getattr(response, "text", "") or ""

        self.messages.append(
            {
                "role": "model",
                "parts": [{"text": ai_reply}],
            }
        )

        return ai_reply