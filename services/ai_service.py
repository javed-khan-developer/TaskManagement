import google.generativeai as genai
from config import GEMINI_API_KEY


class AiService:

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.client = genai

    def chat(self, message: str):
        
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(message)
            return response.text
        