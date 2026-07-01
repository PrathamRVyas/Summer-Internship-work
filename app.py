import streamlit as st
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("Error: OpenAI API key not found.")
    st.info('Add OPENAI_API_KEY="sk-..." to your .env file.')
    st.stop()

st.header("My first Chatbot")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")

if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vector_store = FAISS.from_texts(chunks, embeddings)

    user_question = st.text_input("Type your question here")

    if user_question:
        docs = vector_store.similarity_search(user_question)
        context = "\n\n".join([doc.page_content for doc in docs])

        llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            openai_api_key=OPENAI_API_KEY,
            temperature=0.1,
            max_tokens=1000
        )

        from langchain_core.messages import HumanMessage, SystemMessage

        messages = [
            SystemMessage(content="Answer the question based only on the context provided."),
            HumanMessage(content=f"Context:\n{context}\n\nQuestion: {user_question}")
        ]

        response = llm.invoke(messages)
        st.write(response.content)