import streamlit as st
from dotenv import load_dotenv
load_dotenv()


from ai_engine import generate_response
from prompts import explanation_prompt, summary_prompt, quiz_prompt
from pdf_utils import extract_text_from_pdf
from prompts import pdf_explanation_prompt

if "messages" not in st.session_state:
    st.session_state.messages = []


st.set_page_config("AI Study Buddy", layout="wide")
st.title("🤖 AI Study Buddy")
st.write("Your personal AI-powered learning assistant")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



topic = st.text_input("Enter a topic", 
                      placeholder="e.g., binary search, machine learning, etc.",
                      value="")
    
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

    user_message = topic if not uploaded_pdf else "Explain uploaded PDF"

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_message
    })

    with st.spinner("Thinking..."):

        if uploaded_pdf:
            pdf_text = extract_text_from_pdf(uploaded_pdf)

            if not pdf_text:
                st.error("Could not extract text from PDF.")
                st.stop()

            prompt = pdf_explanation_prompt(
                pdf_text[:12000],   # limit size
                f"{mode} the content"
            )

        elif topic.strip():

            if mode == "Explain":
                prompt = explanation_prompt(topic, level)
            elif mode == "Summarize":
                prompt = summary_prompt(topic)
            else:
                prompt = quiz_prompt(topic)

        else:
            st.warning("Please enter a topic or upload a PDF.")
            st.stop()

        # 🔥 Add chat history to prompt
        chat_history = "\n".join(
            [f"{m['role']}: {m['content']}" for m in st.session_state.messages]
        )

        full_prompt = f"""
Previous conversation:
{chat_history}

Now respond properly:
{prompt}
"""

        result = generate_response(full_prompt)

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": result
    })

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(result)

