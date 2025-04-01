import streamlit as st
import requests

st.set_page_config(page_title="Mistral 7B", page_icon="🤖", layout="centered")

HF_API_KEY = st.secrets["HUGGING_FACE"]
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
HF_API_URL = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Poppins', sans-serif;
    }
.my {
    font-size: 36px;
    font-family: 'Poppins';
    font-weight: bold;
    background: linear-gradient(45deg, 
        #4b4fff, #ff4bff, 
        #4b4fff, #ff4bff, 
        #4b4fff, #ff4bff, 
        #4b4fff, #ff4bff);
    background-size: 400% 400%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 20s infinite linear;
}

@keyframes gradientMove {
    0% {
        background-position: 0% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="my"> Mistral AI</h1>', unsafe_allow_html=True)
st.markdown("Ask me anything and I'll try to answer!")

example_prompts = [
    "Tell me an interesting fact!",
    "How to learn Streamlit",
    "What is AI",
    "Who is Plato?",
    "How to be a better programmer?",
]

col1, col2 = st.columns(2)
for i, prompt in enumerate(example_prompts):
    with (col1 if i % 2 == 0 else col2):
        if st.button(prompt, key=f"btn_{i}"):
            st.session_state.selected_prompt = prompt  

if "huggingface_messages" not in st.session_state:
    st.session_state.huggingface_messages = []
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = ""

for message in st.session_state.huggingface_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  

user_input = st.chat_input("Type your message here...")

prompt = st.session_state.selected_prompt if st.session_state.selected_prompt else user_input

if prompt:
    st.session_state.huggingface_messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)  

    with st.spinner("Thinking... 💭"):
        payload = {"inputs": prompt, "parameters": {"max_length": 512, "temperature": 0.7}}

        try:
            response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
            full_response = data[0]["generated_text"] if isinstance(data, list) else "Invalid response format."
            assistant_response = full_response.replace(prompt, "").strip()  # Remove the prompt if repeated
        except requests.exceptions.RequestException as e:
            assistant_response = f"⚠️ API Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(assistant_response)  

    st.session_state.huggingface_messages.append({"role": "assistant", "content": assistant_response})

    st.session_state.selected_prompt = ""
