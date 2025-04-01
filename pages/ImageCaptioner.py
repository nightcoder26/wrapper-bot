import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="Image Captioning", page_icon="📷", layout="centered")

st.markdown('<h1 class="my"> Salesforce Blip - Image Captioner</h1>', unsafe_allow_html=True)
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

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    HF_API_KEY = st.secrets["HUGGING_FACE"]
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large"
    HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

    with st.spinner("Generating caption..."):
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        response = requests.post(API_URL, headers=HEADERS, json={"image": img_str})

        if response.status_code == 200:
            caption = response.json()[0]["generated_text"]
        else:
            caption = "⚠️ API Error"

    st.write(caption)

