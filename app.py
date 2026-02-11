import streamlit as st
from dotenv import load_dotenv
load_dotenv()


from ai_engine import generate_response
from prompts import explanation_prompt, summary_prompt, quiz_prompt
from pdf_utils import extract_text_from_pdf
from prompts import pdf_explanation_prompt




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

st.subheader("📄 Upload PDF Notes (Optional)")

uploaded_pdf = st.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)

if st.button("Generate", type="primary"):
    if uploaded_pdf:
        with st.spinner("Reading PDF and thinking..."):
            pdf_text = extract_text_from_pdf(uploaded_pdf)

            if not pdf_text:
                st.error("Could not extract text from PDF.")
            else:
                prompt = pdf_explanation_prompt(
                    pdf_text,
                    f"{mode} the content"
                )
                result = generate_response(prompt)
                st.markdown(result)

    elif topic.strip():
        with st.spinner("Thinking..."):
            if mode == "Explain":
                prompt = explanation_prompt(topic, level)
            elif mode == "Summarize":
                prompt = summary_prompt(topic)
            else:
                prompt = quiz_prompt(topic)

            result = generate_response(prompt)
            st.markdown(result)

    else:
        st.warning("Please enter a topic or upload a PDF.")
