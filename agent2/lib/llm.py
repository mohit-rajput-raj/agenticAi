from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

class LLM:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def ask(self, question: str):
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=question,
        )
        return response.text

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "exit":
#         break
#     response = chat.send_message(user_input)
#     print(f"Gemini: {response.text}")