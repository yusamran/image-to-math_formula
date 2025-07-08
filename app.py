import os
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from docx import Document

# Force local model cache
os.environ["TORCH_HOME"] = "./torch_cache"

weights_url = "https://github.com/lukas-blecher/LaTeX-OCR/releases/download/v0.0.1/weights.pth"
weights_path = "./torch_cache/hub/checkpoints/weights.pth"

# Download weights if missing
if not os.path.exists(weights_path):
    st.info("⬇️ Downloading model weights (~50MB)...")
    os.makedirs(os.path.dirname(weights_path), exist_ok=True)
    with requests.get(weights_url, stream=True) as r:
        r.raise_for_status()
        with open(weights_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    st.success("✅ Weights downloaded!")

# Monkey patch to skip site-packages download
import pix2tex.model.checkpoints.get_latest_checkpoint as glc
glc.download_checkpoints = lambda: None

from pix2tex.cli import LatexOCR, Munch

arguments = Munch({
    'config': './settings/config.yaml',
    'checkpoint': weights_path,
    'no_cuda': True,
    'no_resize': False
})

st.title("🧮 Free Image-to-LaTeX Converter (pix2tex)")
uploaded_file = st.file_uploader("Upload", type=["png","jpg","jpeg","bmp","gif","webp"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image)
    if st.button("Convert"):
        model = LatexOCR(arguments)
        latex = model(image)
        st.code(latex)
