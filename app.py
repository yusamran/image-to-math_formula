import streamlit as st
from PIL import Image
from io import BytesIO

from docx import Document

# Import the LaTeX-OCR model
from im2latex import Im2Latex

# Load the model once
@st.cache_resource
def load_model():
    model = Im2Latex()
    return model

model = load_model()

st.title("🧮 Free Image-to-LaTeX Converter")
st.write("Upload an image of a math formula and get LaTeX code. Export to Word too!")

uploaded_file = st.file_uploader("Upload a formula image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Convert to LaTeX"):
        st.info("Processing image... Please wait.")
        latex_result = model.predict(image)

        st.success("✅ Recognized LaTeX:")
        st.code(latex_result)

        # Create Word document with the LaTeX
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
