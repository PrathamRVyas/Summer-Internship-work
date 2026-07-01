import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Fake News Detector", layout="wide")

# sidebar
st.sidebar.title("Fake News Detector")
theme = st.sidebar.selectbox("Theme", ["Dark", "Light"])
st.sidebar.markdown("---")
st.sidebar.markdown("### What this does")
st.sidebar.markdown("Paste any news and the AI will tell you if it looks real or fake.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Steps")
st.sidebar.markdown("1. Paste the news\n2. Fill optional fields\n3. Hit Analyze")
st.sidebar.warning("AI can be wrong sometimes. Always double check.")

# theme
if theme == "Dark":
    st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)
else:
    st.markdown("<style>.stApp { background-color: #f9f9f9; color: black; }</style>", unsafe_allow_html=True)

# main
st.title("Fake News Detector")
st.write("Paste a news headline or article and the AI will analyze it for you.")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    news_text = st.text_area("News Headline or Article", placeholder="Paste news here...", height=180)

with col2:
    source_url = st.text_input("Source URL (optional)", placeholder="https://...")
    language = st.selectbox("Language", ["English", "Hindi", "Gujarati", "Spanish", "Other"])
    category = st.selectbox("Category (optional)", ["Unknown", "Politics", "Health", "Science & Tech", "Sports", "Business"])

st.markdown("---")

if st.button("Analyze"):

    if not news_text.strip():
        st.warning("Please paste something first.")

    else:

        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i + 1)

        with st.spinner("Analyzing..."):

            source_info = f"Source: {source_url}" if source_url.strip() else "No source provided."

            prompt = f"""
Here is a news piece I want you to check:

"{news_text}"

{source_info}
Language: {language}
Category: {category}

Tell me:
1. Is it real, fake, misleading, or unverifiable?
2. How confident are you? (give a %)
3. Why do you think so?
4. Any bias in how it's written?
5. Are the main claims true?
6. What info is missing?
7. How can someone verify this themselves? (3 simple ways)
8. Give a short summary at the end in plain simple english

Don't use complicated words. Write like you're explaining to a regular person.
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a fact-checker. Be straightforward and don't overthink it."},
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content

        st.success("Done!")
        st.markdown("---")
        st.subheader("Result")

        placeholder = st.empty()
        text = ""
        for char in answer:
            text += char
            placeholder.markdown(text)
            time.sleep(0.002)

        st.markdown("---")

    with st.expander("Quick tips"):
        st.markdown("""
    - Google the headline and see what comes up
    - Check the date, old news gets reshared a lot
    - Don't just read the headline, read the full thing
    """)

        st.info("Note: This is AI-generated analysis. Always verify before sharing.")