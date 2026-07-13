from langchain_core.runnables import RunnableBranch , RunnableLambda

def is_long(input: str) -> bool:
    return len(input) > 10

def process_long(input: str) -> str:
    return input.upper()

def process_short(input: str) -> str:
    return input.lower()

# Branch based on condition
branch = RunnableBranch(
    (is_long, RunnableLambda(process_long)),
    RunnableLambda(process_short)  # Default
)

print(branch.invoke("hello"))        # "hello"
print(branch.invoke("hello world!")) # "HELLO WORLD!"