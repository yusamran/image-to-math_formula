import os
import requests
import streamlit as st
from PIL import Image

# --- CONFIG ---
os.environ["TORCH_HOME"] = "./torch_cache"
weights_url = "https://github.com/lukas-blecher/LaTeX-OCR/releases/download/v0.0.1/weights.pth"
weights_path = "./torch_cache/hub/checkpoints/weights.pth"

# --- Download weights ---
def download_weights(url, save_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

if not os.path.exists(weights_path):
    st.info("Downloading weights (~50MB)...")
    download_weights(weights_url, weights_path)
    st.success("✅ Weights downloaded!")

# --- Monkey-patch pix2tex ---
import pix2tex.model.checkpoints.get_latest_checkpoint as glc
def skip_download():
    st.info("✅ Skipping internal download_checkpoints() — using local weights.")
glc.download_checkpoints = skip_download

from pix2tex.cli import LatexOCR

st.info("Loading model...")
model = LatexOCR()
st.success("✅ Model loaded!")

# --- Streamlit UI ---
st.title("🧮 Image to LaTeX OCR")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image")

    if st.button("Convert to LaTeX"):
        st.info("Processing...")
        prediction = model(image)
        st.code(prediction, language="latex")
