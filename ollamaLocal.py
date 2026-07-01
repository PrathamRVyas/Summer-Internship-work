from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain.agents import create_agent
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# Tool 1
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression. 
    Use this ONLY for arithmetic calculations like '2+2', '10*5', '100/4'.
    Input must be a valid Python math expression with numbers and operators only.
    Do NOT use this for general knowledge or text-based questions."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

# Tool 2
@tool
def current_time(dummy: str = "") -> str:
    """Returns the current date and time. 
    Use this when the user asks what time or date it is."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

llm = ChatOllama(model="llama3.2")

Agents = create_agent(
    tools=[calculator, current_time],
    model=llm,
)

# Run
response = Agents.invoke(
    {"messages": [{"role": "user", "content": "What is the date and time right now?"""}]}
)

print(response['messages'][-1].content)