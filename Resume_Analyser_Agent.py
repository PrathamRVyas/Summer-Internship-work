import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
import PyPDF2
import time

llm = OllamaLLM(model="llama3.2")

prompt_template = PromptTemplate(
    input_variables=["resume_text", "job_role"],
    template="""
Here is a student's resume text:

{resume_text}

The job role they are targeting: {job_role}

Please analyze this resume and give me:

1. ATS SCORE - give a score out of 100 and explain why
2. DETECTED SKILLS - list all the skills you found in the resume
3. MISSING SKILLS - list important skills that are missing for the given job role
4. RESUME STRENGTHS - what is already good about this resume
5. IMPROVEMENT SUGGESTIONS - give 4 to 5 practical suggestions to make this resume better
6. OVERALL VERDICT - one short paragraph summarizing if this resume is ready or needs work

Be honest and practical. Write like you're a senior giving feedback to a fresher, not like a formal report.
"""
)

chain = prompt_template | llm

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.sidebar.title("AI Resume Analyzer")
theme = st.sidebar.selectbox("Theme", ["Dark", "Light"])
st.sidebar.markdown("---")
st.sidebar.markdown("### What this does")
st.sidebar.markdown("Upload your resume PDF and the AI will check if it's ATS friendly and ready for your target role.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Steps")
st.sidebar.markdown("1. Upload your resume as PDF\n2. Enter the job role you're targeting\n3. Hit Analyze")
st.sidebar.warning("Make sure your PDF has actual text in it, not just a scanned image.")

if theme == "Dark":
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp { background-color: #f9f9f9; color: black; }</style>", unsafe_allow_html=True)

st.title("AI Resume Analyzer Agent")
st.write("Upload your resume and the AI will analyze it, check ATS compatibility, and suggest improvements.")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Your Resume (PDF only)", type=["pdf"])

with col2:
    job_role = st.text_input("Target Job Role", placeholder="Data Scientist, Backend Developer...")
    st.markdown("")
    st.markdown("")
    if uploaded_file:
        st.success("PDF uploaded successfully!")

st.markdown("---")

if st.button("Analyze Resume"):

    if not uploaded_file:
        st.warning("Please upload your resume first.")

    elif not job_role.strip():
        st.warning("Please enter the job role you are targeting.")

    else:

        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            resume_text = ""
            for page in pdf_reader.pages:
                resume_text += page.extract_text()

            if not resume_text.strip():
                st.error("Could not read text from this PDF. Make sure it's not a scanned image.")

            else:

                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)

                with st.spinner("AI is analyzing your resume..."):
                    answer = chain.invoke({
                        "resume_text": resume_text,
                        "job_role": job_role
                    })

                st.success("Done!")
                st.markdown("---")
                st.subheader("Resume Analysis Report")

                placeholder = st.empty()
                text = ""
                for char in answer:
                    text += char
                    placeholder.markdown(text)
                    time.sleep(0.002)

                st.markdown("---")

        except Exception as e:
            st.error(f"Something went wrong while reading the PDF: {e}")