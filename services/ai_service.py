from openai import OpenAI
from openai import APIStatusError
from openai import RateLimitError

from config import OPENAI_API_KEY


class AiService:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def chat(self, message: str):
        try:
            response = self.client.chat.completions.create(
                model='gpt-4.1-mini',
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI Assistant"
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ]
            )
            return response.choices[0].message.content
        except (RateLimitError, APIStatusError) as exc:
            return (
                "The AI service is temporarily unavailable due to a quota or rate-limit issue. "
                "Please try again later."
            )