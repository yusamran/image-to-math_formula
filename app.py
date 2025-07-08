import os
import urllib.request
import streamlit as st
from PIL import Image
from pix2tex.cli import LatexOCR

# --- CONFIG ---
# Tell torch to use a local, writable cache
os.environ["TORCH_HOME"] = "./torch_cache"
weights_path = "./torch_cache/hub/checkpoints/weights.pth"
weights_url = "https://github.com/lukas-blecher/LaTeX-OCR/releases/download/v0.1/weights.pth"

# --- Download checkpoint if missing ---
if not os.path.exists(weights_path):
    os.makedirs(os.path.dirname(weights_path), exist_ok=True)
    st.info("Downloading model weights... (~50MB)")
    urllib.request.urlretrieve(weights_url, weights_path)
    st.success("✅ Weights downloaded!")

# --- Load model ---
st.info("Loading model...")
model = LatexOCR()
st.success("✅ Model loaded!")

# --- Streamlit UI ---
st.title("🧮 Image to LaTeX OCR")

uploaded_file = st.file_uploader("Upload an image of a formula", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Convert to LaTeX"):
        st.info("Processing...")
        prediction = model(image)
        st.code(prediction, language="latex")
