import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from PyPDF2 import PdfReader

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("PDF Chatbot")

pdf = st.file_uploader("Upload PDF", type="pdf")

if pdf:
    text = ""

    reader = PdfReader(pdf)

    for page in reader.pages:
        text += page.extract_text()

    question = st.text_input("Ask a question")

    if question:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "user",
                    "content": f"""
                    PDF Content:
                    {text}

                    Question:
                    {question}
                    """
                }
            ]
        )

        st.write(response.choices[0].message.content)