import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

MODEL_NAME = "gemini-1.5-pro"
st.set_page_config(page_title="Gemini 1.5 Pro Chatbot", page_icon="🤖", layout="centered")
st.markdown('<h1 class="my">Gemini 1.5 Pro Chatbot</h1>', unsafe_allow_html=True)
st.markdown("Ask me anything and I'll try to answer!")

example_prompts = [
    "Tell me an interesting fact!",
    "How to learn Streamlit",
    "What is AI",
    "Who is Plato?",
    "How to be a better programmer?",
]
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }
     .my {
        color: #4b4fff !important; 
        font-size: 36px; 
        font-family: 'Poppins';
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns(2)
for i, prompt in enumerate(example_prompts):
    with (col1 if i % 2 == 0 else col2):
        if st.button(prompt, key=f"btn_{i}"):
            st.session_state.selected_prompt = prompt  # Store selected prompt

if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = ""

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input("Ask me anything...")

prompt = st.session_state.selected_prompt if st.session_state.selected_prompt else user_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    with st.chat_message("assistant"):
        st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})

    st.session_state.selected_prompt = ""
