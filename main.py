import io
import streamlit as st
from huggingface_hub import InferenceClient
import config

st.set_page_config(page_title="AI Avatar Creator", page_icon="🎨", layout="centered")

OPTIONS = {
    "avatar type": ["boy hero", "girl hero", "wizard", "robot explorer", "space warrior", "animal adventurer"],
    "hairstyle": ["short spiky hair", "curly hair", "long straight hair", "ponytail", "glowing hair", "helmet"],
    "outfit": ["superhero suit", "magical robe", "space armor", "casual hoodie", "battle costume", "royal outfit"],
    "expression": ["happy", "confident", "excited", "brave", "mysterious", "playful"],
    "background": ["forest", "space station", "magic castle", "city skyline", "rainbow world", "cloud kingdom"],
    "art style": ["cartoon style", "anime style", "3D game style", "fantasy illustration", "comic style"],
}

client = InferenceClient(api_key=config.HF_API_KEY)
st.session_state.setdefault("generated_image", None)

st.title(" AI Avatar Creator")
st.write("Create Your own avatar with AI!")
st.markdown("Choose your Avatar details write your own custom prompt,then click** Generate Avatar **.")
st.subheader(" Create Your Avatar")

mode = st.selectbox("Choose prompt mode", ["Use Avatar Builder", "Write Custom Prompt"])

if mode == "Use Avatar Builder":
    values = {k: st.selectbox(f"Choose {k}", v) for k, v in
OPTIONS.item()}
    extra = st.text_input("Add one extra detail (optional)",
placeholder="Example: glowing blue eyes").strip()
    prompt = (
        f"A kid-friendly {values['avatar type']}, "
        f"with {values['hairstyle']}, "
        f"wearing {values['outfit']}, "
        f"with a {values['expression']} expression, "
        f"in a {values['background']} background, "
        f"{values['art style']}, colorful, highly detailed, digital"
    )