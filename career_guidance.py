import streamlit as st
from openai import OpenAI
from datetime import datetime
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)


st.set_page_config(
    page_title="AI Career Mentor Agent",
    layout="wide"
)

st.sidebar.title("AI Career Mentor")

theme = st.sidebar.selectbox(
    "Choose Theme",
    ["Dark", "Light"]
)

effect = st.sidebar.selectbox(
    "Choose Celebration Effect",
    ["Balloons", "Snow"]
)

st.sidebar.markdown("---")

st.sidebar.info(
    """
    This AI Agent helps students with:

     - Career Guidance  
     - Project Ideas  
     - Internship Suggestions  
     - Learning Roadmaps  
    """
)


if theme == "Dark":

    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

else:

    st.markdown("""
        <style>
        .stApp {
            background-color: white;
            color: black;
        }
        </style>
    """, unsafe_allow_html=True)


st.title(" AI Career Mentor Agent")

st.write(
    "Get personalized career guidance, project ideas, internship suggestions, and learning roadmaps using AI."
)

with st.container():

    st.subheader("Student Profile")

    skills = st.text_input(
        "Enter Your Skills",
        placeholder="Python, HTML, CSS"
    )

    interests = st.text_input(
        "Enter Your Interests",
        placeholder="AI, Machine Learning, Web Development"
    )

    goal = st.text_input(
        "Enter Your Career Goal",
        placeholder="Secure AI Internship"
    )


if st.button("Generate Career Advice"):

    # VALIDATION

    if not skills or not interests or not goal:

        st.warning("⚠Please fill all fields.")

    else:

       
        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        with st.spinner("AI Agent is analyzing your profile..."):

            

            prompt = f"""
            You are an intelligent AI Career Mentor Agent.

            Analyze the student's profile carefully.

            Skills: {skills}
            Interests: {interests}
            Career Goal: {goal}

            Provide:

            1. Best Career Paths
            2. Skills To Improve
            3. Best Projects To Build
            4. Internship Suggestions
            5. 30-Day Learning Roadmap
            6. Motivation Tip

            Use beginner-friendly and simple language.
            """

            

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response.choices[0].message.content

            st.success("✅Career Guidance Generated Successfully!")

      
            if effect == "Balloons":
                st.balloons()
            else:
                st.snow()

            
            st.subheader("🤖 AI Mentor Response")

            typing_placeholder = st.empty()

            displayed_text = ""

            for char in answer:
                displayed_text += char
                typing_placeholder.markdown(displayed_text)
                time.sleep(0.002)
                

                          
            st.info("💾 Memory Saved Successfully!")