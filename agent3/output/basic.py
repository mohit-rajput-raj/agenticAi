from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import FakeListChatModel

# Define a Pydantic model
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")

# Create parser
parser = PydanticOutputParser(pydantic_object=Joke)

# Build prompt with format instructions
prompt = ChatPromptTemplate.from_messages([
    ("system", "Answer in JSON format. {format_instructions}"),
    ("human", "Tell me a joke about chickens."),
]).partial(format_instructions=parser.get_format_instructions())

# Mock LLM (returns valid JSON)
chat_llm = FakeListChatModel(responses=[
    '{"setup": "Why did the chicken cross the road?", "punchline": "To get to the other side!"}'
])

# Chain: prompt -> LLM -> parser
chain = prompt | chat_llm | parser

# Invoke
joke = chain.invoke({})
print(joke)
# Output: Joke(setup='Why did the chicken cross the road?', punchline='To get to the other side!')