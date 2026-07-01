from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,   
    model="gpt-3.5-turbo",
    temperature=0.1
)

Prompt = PromptTemplate(
    input_variables=["Batsman", "Bowler", "Match_Situation"],
    template="""
    You are a legendary cricket commenatator.
    Generate energetic cricket commentary based on 
    batsman = {Batsman}
    bowler = {Bowler}
    situation = {Match_Situation}

    Requirements:
    - Keep commentary under 150 words
    - Talk like Ian Bishop
    - Energetic
"""
)

Batsman = input("Enter batsman name:")

Bowler = input("Enter bowler name:")

Match_Situation = input("Enter match situation:")


final_prompt = Prompt.format(
    Batsman=Batsman,
    Bowler=Bowler,
    Match_Situation=Match_Situation,
)

response = llm.invoke(final_prompt)

print("\nAI Cricket Commentary:\n")
print(response.content)