import base64
from io import BytesIO

import streamlit as st
from PIL import Image
from groq import Groq
import config

st.set_page_config(page_title="AI Visionary", page_icon="🕵️", layout="centered")

STYLES = {
    "Normal": (
        "Look at this image carefully and write a clear, detailed report. "
        "Describe the scene, objects, and what seems to be happening."
    ),
    "Funny": (
        "Look at this image carefully and write a funny image report. "
        "Mention objects, details, and make the report playful and humorous, "
        "but still describe the image correctly."
    ),
    "Detective": (
        "Look at this image like a detective. "
        "Write an investigation-style report with clues, observations, and smart deductions."
    ),
    "Dramatic": (
        "Look at this image and describe it in a dramatic, cinematic way. "
        "Make the report vivid, exciting, and expressive."
    ),
    "Story Mode": (
        "Look at this image and write a short story-like scene description. "
        "Describe the setting, objects, and mood in a creative way."
    ),
}

client = Groq(api_key=config.GROQ_API_KEY)

# -------------------------------
# Next Steps:
# 1. Add page title, description, and instructions
# 2. Create a helper function to analyze the uploaded image
# 3. Add file uploader for image input
# 4. Add report style selection using STYLES
# 5. Preview the uploaded image on the screen
# 6. Add button to send the image to the Groq Vision model
# 7. Display the generated AI report
# 8. Add error handling for missing API key, missing image, or API issues
# -------------------------------