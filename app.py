import streamlit as st
from PIL import Image
from io import BytesIO
import subprocess
import tempfile
import os

from docx import Document

# ----------------------------
# Title + Instructions
# ----------------------------
st.title("🧮 Free Image-to-LaTeX Converter")
st.write(
    "Upload an image of a math formula (PNG, JPG, JPEG, BMP, GIF, WEBP — "
    "any case) and get the recognized LaTeX code. "
    "You can also export it to a Word file!"
)

# ----------------------------
# ✅ Safe file uploader — lowercased, no dot, no duplicate
# Streamlit normalizes extensions internally, so this works for any case.
# ----------------------------
uploaded_file = st.file_uploader(
    "Upload a formula image",
    type=["png", "jpg", "jpeg", "bmp", "gif", "webp"]
)

if uploaded_file:
    st.info("✅ Allowed file types: png, jpg, jpeg, bmp, gif, webp (case-insensitive)")
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Convert to LaTeX"):
        st.info("⏳ Processing image... This may take 10–30 sec.")

        # Save uploaded image to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            image.save(tmp.name)
            image_path = tmp.name

        # ✅ Run LaTeX-OCR predict.py via subprocess
        # Make sure you cloned LaTeX-OCR in your project folder!
        command = f"python LaTeX-OCR/predict.py --img {image_path} --config LaTeX-OCR/config.yaml"

        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            latex_result = result.stdout.strip()
            st.success("✅ Recognized LaTeX:")
            st.code(latex_result)

            # Export to Word
            doc = Document()
            doc.add_paragraph("Recognized LaTeX formula:")
            doc.add_paragraph(latex_result)

            buffer = BytesIO()
            doc.save(buffer)
            buffer.seek(0)

            st.download_button(
                label="📄 Download Word File",
                data=buffer,
                file_name="formula.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        else:
            st.error("❌ Something went wrong. Error details:")
            st.error(result.stderr)

        os.unlink(image_path)  # Clean up temp file

else:
    st.info("ℹ️ Allowed file types: png, jpg, jpeg, bmp, gif, webp (case-insensitive)")
