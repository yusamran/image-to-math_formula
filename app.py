import streamlit as st
from PIL import Image
from io import BytesIO
import os
from docx import Document
# ✅ Tell torch to use your local writable path
os.environ["TORCH_HOME"] = "./torch_cache"
from pix2tex.cli import LatexOCR
model = LatexOCR()
# ----------------------------
# App title & instructions
# ----------------------------
st.title("🧮 Free Image-to-LaTeX Converter (pix2tex)")
st.write(
    "Upload an image of a math formula (PNG, JPG, JPEG, BMP, GIF, WEBP — "
    "any case) and get the recognized LaTeX code. "
    "You can also export it to a Word file!"
)

# ----------------------------
# ✅ File uploader (case-insensitive, no dot, no duplicates)
# Streamlit normalizes extensions.
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

        # ✅ Use pix2tex directly
        model = LatexOCR()
        latex_result = model(image)

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
    st.info("ℹ️ Allowed file types: png, jpg, jpeg, bmp, gif, webp (case-insensitive)")
