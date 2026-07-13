from langchain_core.prompts import PromptTemplate

template = """tell me {adjective} news about {city}"""
prompt = PromptTemplate.from_template(template)
preFilled_prompt = prompt.partial(adjective="funny")

print(preFilled_prompt.format(city="New York"))
