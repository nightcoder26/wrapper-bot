import streamlit as st
import requests

st.set_page_config(page_title="BART Summarization", page_icon="🤖", layout="centered")

HF_API_KEY = st.secrets["HUGGING_FACE"]
MODEL_NAME = "facebook/bart-large-cnn"
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

st.markdown('<h1 class="my"> BART Summarization</h1>', unsafe_allow_html=True)
st.markdown("Provide me with text, and I'll summarize it for you!")

example_prompts = [
    "Summarize the following text: The AI revolution is happening all around us, from healthcare to business, the pace of innovation is accelerating. Many industries are being transformed, and it's important to stay up-to-date with the latest trends.",
    "Summarize the following text: The internet has revolutionized the way we communicate, share information, and connect with each other. Social media platforms, in particular, have created a new avenue for global interaction.",
    "Summarize the following text: Machine learning is a subset of artificial intelligence that focuses on building algorithms that enable machines to learn from data. It is becoming an integral part of many applications, from recommendation systems to autonomous vehicles."
]

col1, col2 = st.columns(2)
for i, prompt in enumerate(example_prompts):
    with (col1 if i % 2 == 0 else col2):
        if st.button(f"Example {i+1}", key=f"btn_{i}"):
            st.session_state.selected_prompt = prompt  

if "huggingface_messages" not in st.session_state:
    st.session_state.huggingface_messages = []
if "selected_prompt" not in st.session_state:
    st.session_state.selected_prompt = ""

for message in st.session_state.huggingface_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])  

user_input = st.chat_input("Type the text you want to summarize here...")

prompt = st.session_state.selected_prompt if st.session_state.selected_prompt else user_input

if prompt:
    st.session_state.huggingface_messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)  

    with st.spinner("Summarizing... 💭"):
        payload = {"inputs": prompt, "parameters": {"max_length": 512, "temperature": 0.7}}

        try:
            response = requests.post(HF_API_URL, headers=HEADERS, json=payload)
            response.raise_for_status()
            data = response.json()
            summary = data[0]["summary_text"] if isinstance(data, list) else "Invalid response format."
        except requests.exceptions.RequestException as e:
            summary = f"⚠️ API Error: {str(e)}"

    with st.chat_message("assistant"):
        st.markdown(summary)  

    st.session_state.huggingface_messages.append({"role": "assistant", "content": summary})

    st.session_state.selected_prompt = ""
