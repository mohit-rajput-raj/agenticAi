from google import genai
from google.genai import types
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

    def extract_table_data(self, image_bytes: bytes, mime_type: str) -> str:
        image_part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
        prompt = "Extract all data from the tables in this image. Return the extracted data as valid JSON. Ensure all rows and columns are accurately represented. if difficult to predict a row or column or a cell  value set it to 'N/A'"
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[image_part, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return response.text

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "exit":
#         break
#     response = chat.send_message(user_input)
#     print(f"Gemini: {response.text}")