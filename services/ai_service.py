from google import genai
from config import GEMINI_API_KEY


class AiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.messages = []

    def chat(self, messages: list):

        self.messages.append(
            {
                "role": "user",
                "parts": [{"text": messages}]
            }
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=self.messages
        )

        ai_reply = response.text

        self.messages.append(
            {
                "role": "model",
                "parts": [{"text": ai_reply}]
            }
        )

        return ai_reply