from langchain_core.runnables import RunnableParallel ,RunnableLambda

def get_name(input: dict) -> str:
    return input["name"]

def get_age(input: dict) -> int:
    return input["age"]

# Define parallel steps
parallel = RunnableParallel(
    name=RunnableLambda(get_name),
    age=RunnableLambda(get_age)
)

# Invoke
result = parallel.invoke({"name": "Alice", "age": 30})
print(result)  # {"name": "Alice", "age": 30}