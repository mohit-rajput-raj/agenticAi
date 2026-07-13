import asyncio

from langchain_core.runnables import RunnableLambda , RunnableSequence

# Define a simple function
def add_five(x: int) -> int:
    return x + 5
def uppercase(input: str) -> str:
    return input.upper()

def add_exclamation(input: str) -> str:
    return input + "!"

async def async_reverse(input: str) -> str:
    return input[::-1]
# Wrap it in a Runnable
turnToUpperCase_runnable = RunnableLambda(uppercase)
add_exclamation_runnable = RunnableLambda(add_exclamation)
async_reverse_runnable = RunnableLambda(async_reverse)

add_five_runnable = RunnableLambda(add_five)

# Invoke it
result = add_five_runnable.invoke(3)
chain = async_reverse_runnable | turnToUpperCase_runnable | add_exclamation_runnable
print(result)  # Output: 8
res = asyncio.run(chain.ainvoke("DLrow OllEH"))
print(res)  # Output: "!DLROW OLLEH"
sec = RunnableSequence(
    RunnableLambda(uppercase) ,RunnableLambda(add_exclamation),RunnableLambda(async_reverse)
)
print(asyncio.run(sec.ainvoke("hello world")))  # Output: "!DLROW OLLEH"