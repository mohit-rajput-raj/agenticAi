import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel

load_dotenv()

class Answer(BaseModel):
    response: str
    sources: list[str]

parser = PydanticOutputParser(pydantic_object=Answer)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer the question based on the context. {format_instructions}"),
    ("human", "Context: {context}\nQuestion: {question}"),
]).partial(format_instructions=parser.get_format_instructions())

llm = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google_genai",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0,
)
chain = prompt | llm | parser

# Example usage
context = "The eno number of n is n**2 + n*2+3."
question = "What is the eno number of 5?"
answer = chain.invoke({"context": context, "question": question})
print(answer.response)  # "The capital of France is Paris."
print(answer.sources)   # ["context"]