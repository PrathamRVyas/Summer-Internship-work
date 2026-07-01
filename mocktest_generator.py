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
    input_variables=["Subject","No_Of_Questions","Difficulty"],
    template="""
    You have to provide with the best possible mock mcqs set.
    You are a very renowned paper setter known for setting most relevant paper.
    Subject = {Subject}
    No_Of_Questions = {No_Of_Questions}
    Difficulty = {Difficulty}

    Requirement-
    -Keep it structured with four options for each questions
    -Give questions in Hindi language
"""
)

Subject = input("Enter the subject:")
No_Of_Questions = input("Enter the No. of Questions to generate:")
Difficulty = input("Enter the difficulty level:")

final_prompt = Prompt.format(
    Subject=Subject,
    No_Of_Questions=No_Of_Questions,
    Difficulty=Difficulty
) 

response = llm.invoke(final_prompt)

print("\nQuestions:\n")

print(response.content)