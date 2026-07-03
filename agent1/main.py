from google import genai
import os
from dotenv import load_dotenv
import sympy as sp

load_dotenv()

# --- Tool Definitions ---

def calculate(equation: str) -> str:
    """Evaluates a mathematical expression given as a string (e.g., '2*x + 3')."""
    try:
        return str(sp.sympify(equation))
    except Exception as e:
        return str(e)

def differential_calculus(equation: str, diff_var: str) -> str:
    """Calculates the derivative of an equation with respect to a variable."""
    try:
        # Convert string to expression and derive
        expr = sp.sympify(equation)
        var = sp.symbols(diff_var)
        return str(sp.diff(expr, var))
    except Exception as e:
        return str(e)

def multiply(a: int, b: int) -> int:
    """Multiplies two integers together."""
    return a * b

# --- Agent Setup ---

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Pass all your functions into the tools list
chat = client.chats.create(
    model="gemini-2.5-flash",
    config={"tools": [calculate, differential_calculus, multiply]}
)

# Test the agent with a complex request
# response = chat.send_message("Find the derivative of x**2 + 3*x with respect to x")
# print(f"Gemini: {response.text}")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chat.send_message(user_input)
    print(f"Gemini: {response.text}")