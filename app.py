import os
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
from docx import Document

# ----------------------------
# ✅ Local torch cache config
# ----------------------------
os.environ["TORCH_HOME"] = "./torch_cache"

weights_url = "https://github.com/lukas-blecher/LaTeX-OCR/releases/download/v0.0.1/weights.pth"
weights_path = "./torch_cache/hub/checkpoints/weights.pth"

# ✅ Download weights if missing
if not os.path.exists(weights_path):
    st.info("⬇️ Downloading model weights (~50MB)...")
    os.makedirs(os.path.dirname(weights_path), exist_ok=True)
    with requests.get(weights_url, stream=True) as r:
        r.raise_for_status()
