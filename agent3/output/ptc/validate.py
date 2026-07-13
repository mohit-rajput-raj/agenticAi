from pydantic import BaseModel, field_validator
from langchain_core.output_parsers import PydanticOutputParser 
class User(BaseModel):
    name: str
    age: int

    @field_validator("age")
    def check_age(cls, v):
        if v < 0 or v > 120:
            raise ValueError("Age must be between 0 and 120")
        return v

parser = PydanticOutputParser(pydantic_object=User)
print(parser.get_format_instructions())