import streamlit as st
from dotenv import load_dotenv
load_dotenv()


from ai_engine import generate_response
from prompts import explanation_prompt, summary_prompt, quiz_prompt



st.set_page_config("AI Study Buddy", layout="wide")
st.title("🤖 AI Study Buddy")
st.write("Your personal AI-powered learning assistant")

topic = st.text_input("Enter a topic", 
                      placeholder="e.g., binary search, machine learning, etc.",
                      value="binary search")

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Explain", "Summarize", "Quiz"]
)

level = st.sidebar.selectbox(
    "Explanation Level",
    ["Beginner", "Intermediate", "Exam-Ready"]
)

# 6️⃣ Generate button
if st.button("Generate", type="primary"):
    if not topic.strip():
        st.warning("Please enter a topic")
    else:
        with st.spinner("Thinking..."):
            if mode == "Explain":
                prompt = explanation_prompt(topic, level)
            elif mode == "Summarize":
                prompt = summary_prompt(topic)
            else:
                prompt = quiz_prompt(topic)

            try:
                result = generate_response(prompt)
                st.markdown(result)
            except Exception as e:
                st.error("Something went wrong while generating the response.")
                st.exception(e)
