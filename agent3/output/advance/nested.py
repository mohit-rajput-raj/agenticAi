from typing import List
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel , Field , create_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_community.chat_models import FakeListChatModel
load_dotenv()

class Author(BaseModel):
    name: str
    age: int

class Book(BaseModel):
    title: str
    author: Author
    genres: List[str]

parser = PydanticOutputParser(pydantic_object=Book)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer in JSON format. {format_instructions}"),
    ("human", "Tell me about a book."),
]).partial(format_instructions=parser.get_format_instructions())

model = init_chat_model(model="gemini-2.5-flash", model_provider="google_genai", api_key=os.getenv("GEMINI_API_KEY"))

chain = prompt | model | parser
try:
    book = chain.invoke({})
except Exception:
    fallback_model = FakeListChatModel(
        responses=[
            '{"title": "The Hobbit", "author": {"name": "J.R.R. Tolkien", "age": 122}, "genres": ["Fantasy", "Adventure"]}'
        ]
    )
    chain = prompt | fallback_model | parser
    book = chain.invoke({})

print(book.author.name)  # "J.R.R. Tolkien"