import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import json
import re

st.set_page_config(page_title="AI Mock Code Reviewer", layout="wide")

st.sidebar.title("AI Mock Code Reviewer")
st.sidebar.write("A local AI agent that reviews your code and grades it like a senior developer would.")
st.sidebar.markdown("---")
st.sidebar.markdown("### How to use it")
st.sidebar.markdown("1. Pick your language\n2. Pick a coding standard\n3. Paste your code\n4. Hit Review Code")
st.sidebar.markdown("---")
st.sidebar.markdown("### What you get")
st.sidebar.markdown("- A letter grade\n- Bugs and vulnerabilities\n- Optimization tips\n- A refactored version side by side")
st.sidebar.markdown("---")
st.sidebar.caption("Runs fully local through Ollama, no code leaves your machine.")

st.title("AI Mock Code Reviewer")

language = st.selectbox("Programming Language", ["Python", "Java", "JavaScript", "C++", "TypeScript", "Go"])
standard = st.selectbox("Target Coding Standard", ["PEP 8", "Clean Code", "Google Style Guide", "Airbnb Style Guide"])
code_input = st.text_area("Paste your code here", height=250)

SYSTEM_PROMPT = (
    "You are a senior code reviewer analyzing {language} code against the {standard} standard. "
    "Review the code for bugs, logical errors, edge cases, and security vulnerabilities. "
    "Suggest optimizations and provide a refactored version of the code. "
    "Respond with ONLY valid JSON, no markdown fences, no extra text, in this structure: "
    '{{"score": "B+", "issues": [], "optimizations": [], "refactored_code": "", "suggestions": []}}'
)

prompt = ChatPromptTemplate.from_messages([("system", SYSTEM_PROMPT), ("human", "{code}")])
llm = ChatOllama(model="llama3", temperature=0.2, format="json")
chain = prompt | llm | StrOutputParser()

if st.button("Review Code"):
    if not code_input.strip():
        st.warning("Paste some code first.")
    else:
        with st.spinner("Reviewing code..."):
            try:
                raw = chain.invoke({"language": language, "standard": standard, "code": code_input})
                result = json.loads(raw)
            except Exception as e:
                st.error("Something went wrong. Make sure Ollama is running locally.")
                st.caption(str(e))
                result = None

        if result:
            st.metric("Code Score", result.get("score", "N/A"))

            st.subheader("Identified Issues")
            for issue in result.get("issues", []):
                st.markdown(f"- {issue}")

            st.subheader("Optimization Suggestions")
            for opt in result.get("optimizations", []):
                st.markdown(f"- {opt}")

            st.subheader("Before and After")
            col1, col2 = st.columns(2)
            with col1:
                st.code(code_input, language=language.lower())
            with col2:
                st.code(result.get("refactored_code", ""), language=language.lower())

            st.subheader("Suggestions")
            for s in result.get("suggestions", []):
                st.markdown(f"- {s}")