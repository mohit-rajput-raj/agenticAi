from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate # Use ChatPromptTemplate for chat models
from pydantic import create_model
import os

load_dotenv()

# 1. Schema for input
JokeRequest = create_model("JokeRequest", adjective=(str, ...), topic=(str, ...))

# 2. Use ChatPromptTemplate for better compatibility with chat models
prompt = ChatPromptTemplate.from_template("Tell me a {adjective} joke about {topic}.")

# 3. Initialize model
model = init_chat_model(
    model="gemini-1.5-flash", # Ensure you are using a valid model string
    model_provider="google_genai"
    ,api_key=os.getenv("GEMINI_API_KEY"),
)

# 4. Chain
chain = prompt | model

if __name__ == "__main__":
    # Simulate input
    data = {"adjective": "funny", "topic": "chickens"}
    
    # Invoke chain
    response = chain.invoke(data)
    
    print("Model response:")
    print(response.content)