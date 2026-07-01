from langchain import agents
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import create_agent
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


#Tool 1
@tool
def calculator(expression: str):
    """Useful for solving real world math problems."""
    return str(eval(expression))

#Tool 2
@tool
def current_time(text:str):
    """Useful for getting the current date and time."""
    return datetime.now()

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,   
    model="gpt-3.5-turbo"
)

Agents=create_agent(
    tools=[calculator,current_time],
    model=llm,
)

#Run
response = Agents.invoke(
    {"messages":[{"role":"user","content": "What is Machine Learning?"}]}
)

print(response['messages'][-1].content)
