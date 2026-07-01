import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import time

llm = OllamaLLM(model="llama3.2")

prompt_template = PromptTemplate(
    input_variables=["skills", "domain", "interests", "duration"],
    template="""
A student wants ideas for their final year project. Here are their details:

Skills: {skills}
Domain: {domain}
Interests: {interests}
Project Duration: {duration}

Generate 5 project ideas for them. For each project give:

1. PROJECT NAME - a clear and interesting name
2. DESCRIPTION - 2 to 3 lines explaining what the project does
3. TECH STACK - list the tools and technologies to use
4. ARCHITECTURE - briefly explain how the system is structured (frontend, backend, AI components etc)
5. KEY MODULES - list the main modules or features to build
6. WEEK BY WEEK TIMELINE - break the project into weeks based on the duration given
7. DIFFICULTY LEVEL - Easy / Medium / Hard and why

Make the ideas practical and buildable by a final year student. Don't suggest anything too basic like a simple calculator or too complex like building a new AI model from scratch. Think of real world useful projects.
"""
)

chain = prompt_template | llm

st.set_page_config(page_title="AI Project Idea Generator", layout="wide")

st.sidebar.title("AI Project Idea Generator")
theme = st.sidebar.selectbox("Theme", ["Dark", "Light"])
st.sidebar.markdown("---")
st.sidebar.markdown("### What this does")
st.sidebar.markdown("Enter your skills and interests and the AI will suggest 5 final year project ideas with full details.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Steps")
st.sidebar.markdown("1. Fill in your profile\n2. Pick project duration\n3. Hit Generate")
st.sidebar.warning("Pick a project you're actually interested in, not just the easiest one.")

if theme == "Dark":
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp { background-color: #f9f9f9; color: black; }</style>", unsafe_allow_html=True)

st.title("AI Project Idea Generator Agent")
st.write("Not sure what to build for your final year project? Fill in your details and let the AI suggest ideas that actually match your skills and goals.")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    skills = st.text_input("Your Skills", placeholder="Python, React, Machine Learning, SQL...")
    interests = st.text_input("Your Interests", placeholder="Healthcare, Finance, Education, Social Media...")

with col2:
    domain = st.text_input("Your Domain / Field", placeholder="AI, Web Development, Cybersecurity...")
    duration = st.selectbox("Project Duration", ["1 Month", "2 Months", "3 Months", "6 Months"])

st.markdown("---")

if st.button("Generate Project Ideas"):

    if not skills.strip() or not interests.strip() or not domain.strip():
        st.warning("Please fill in all the fields first.")

    else:

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        with st.spinner("AI is thinking of project ideas for you..."):
            answer = chain.invoke({
                "skills": skills,
                "domain": domain,
                "interests": interests,
                "duration": duration
            })

        st.success("Done!")
        st.markdown("---")
        st.subheader("Your Project Ideas")

        placeholder = st.empty()
        text = ""
        for char in answer:
            text += char
            placeholder.markdown(text)
            time.sleep(0.002)

        st.markdown("---")

       