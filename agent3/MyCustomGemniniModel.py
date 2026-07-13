import os
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

class Model:
    def __init__(self, model_name: str = "gemini-2.5-flash", temperature: float = 0.7):
        # Retrieve the key explicitly
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")

        self.llm = init_chat_model(
            model=model_name,
            model_provider="google_genai",
            temperature=temperature,
            google_api_key=api_key  # Pass the key explicitly here
        )

    def get_llm(self):
        return self.llm