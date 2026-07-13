from typing import List
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

load_dotenv()

class Author(BaseModel):
    name: str
    age: int

class Book(BaseModel):
    title: str
    author: Author
    genres: List[str]

# 1. Initialize the model
model = init_chat_model(
    model="gemini-2.5-flash", 
    model_provider="google_genai", 
    api_key=os.getenv("GEMINI_API_KEY")
)

# 2. Use .with_structured_output to force the model to return the Pydantic class
structured_model = model.with_structured_output(Book)

# 3. Create the prompt (no need for manual parser instructions)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that returns book information."),
    ("human", "Tell me about a classic book."),
])

# 4. Chain
chain = prompt | structured_model

# 5. Invoke
book = chain.invoke({})
print(f"Title: {book.title}")
print(f"Author: {book.author.name}")