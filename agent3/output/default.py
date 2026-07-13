from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser 
from langchain_community.chat_models import FakeListChatModel
from langchain_core.prompts import ChatPromptTemplate
class User(BaseModel):
    name: str
    age: int = Field(ge=0, le=120, description="Age must be between 0 and 120")
    email: str | None = None  # Optional field

parser = PydanticOutputParser(pydantic_object=User)
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer in JSON format"),
    ("human", "what is your name, age, and email?"),
]).partial(format_instructions=parser.get_format_instructions())
# LLM returns partial data (age missing)
chat_llm = FakeListChatModel(responses=['{"name": "Alice", "age": 30}'])

chain = prompt | chat_llm | parser
user = chain.invoke({})
print(user)  # None (default)