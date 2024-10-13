import streamlit as st
import easyocr
from PIL import Image
import tempfile

@st.cache_resource
def load_model():
    reader = easyocr.Reader(['pt', 'en'], gpu=False)
    return reader

reader = load_model()

st.header("OCR para imagem de matrículas")

matricula_original = st.file_uploader("Selecione a foto da matrícula que deseja", type=['png', 'jpg', 'jpeg', 'tif', 'tiff'])

@st.cache_data(show_spinner="Extraindo texto da matrícula...")
def process_image(image_file):

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_image:
        temp_image.write(image_file.read())

        image = Image.open(temp_image.name)

        with st.spinner("Extraindo texto da matrícula..."):
            text_results = reader.readtext(temp_image.name, detail=0)

        texto_matricula = ' '.join(text_results)
    return texto_matricula

if matricula_original is not None:
    texto_extraido = process_image(matricula_original)
    st.subheader("Texto extraído:")
    st.write(texto_extraido)


if matricula_original is not None:
    if st.button("Enviar"):

        texto_laudo = process_image()
        expander = st.expander("Texto Extraído do Laudo Original")
        expander.write(texto_laudo)