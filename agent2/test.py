import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.tools import tool
# from langchain.memory import InMemorySaver
from pydantic import BaseModel , Field
load_dotenv()



chat_model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
)
agent = create_agent(
    model=chat_model,
    tools=[],
   
)

response = agent.invoke({"messages": [{"role": "user", "content": "Tell me about a movir promethuse"}]})
movie_info = response['structured_response']
print(movie_info)
