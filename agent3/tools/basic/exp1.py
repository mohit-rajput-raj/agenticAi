from langchain_core.tools import tool

# Define a tool with @tool decorator
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"Sunny in {city}"

# Invoke the tool directly
print(get_weather.invoke({"city": "Paris"}))  # "Sunny in Paris"

# Or call it like a function
print(get_weather.func("Paris"))  # "Sunny in Paris"

@tool
def calculate_area(length: float, width: float) -> float:
    """Calculate the area of a rectangle."""
    return length * width

# Invoke with arguments
area = calculate_area.invoke({"length": 5.0, "width": 3.0})
print(area)  # 15.0

@tool
def greet(name: str, greeting: str = "Hello") -> str:
    """Greet a person with an optional custom greeting."""
    return f"{greeting}, {name}!"

print(greet.invoke({"name": "Alice"}))  # "Hello, Alice!"
print(greet.invoke({"name": "Bob", "greeting": "Hi"}))  # "Hi, Bob!"





import asyncio

@tool
async def fetch_data(url: str) -> str:
    """Fetch data from a URL (async)."""
    await asyncio.sleep(0.1)  # Simulate async I/O
    return f"Data from {url}"

# Invoke async tool
async def main():
    result = await fetch_data.ainvoke({"url": "https://api.example.com"})
    print(result)  # "Data from https://api.example.com"

asyncio.run(main())