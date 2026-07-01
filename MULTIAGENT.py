from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def calculator(expression: str):
    """Useful for solving math problems."""
    return str(eval(expression))

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    api_key=OPENAI_API_KEY
)

math_agent = initialize_agent(
    tools=[calculator],
    model=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

question = input("Ask: ")

if any(op in question for op in ["+","-","*","/"]):
    print(math_agent.run(question))
else:
    print(llm.invoke(question).content)