import streamlit as st
import cv2
import numpy as np
from PIL import Image
from streamlit.runtime.uploaded_file_manager import UploadedFile
from ultralytics import YOLO
from datetime import datetime
from modules.history import create_connection
from .model import load_model


def get_file_name(uploaded_file: UploadedFile) -> str:
    return (
        uploaded_file.name
        + "_"
        + str(datetime.now().strftime("%Y%m%d%H%M%S"))
        + "."
        + uploaded_file.type.split("/")[1]
    )


def save_analysis(
    uploaded_file: UploadedFile, has_person: bool, has_hardhat: bool, employee_name: str
) -> None:

    file_path = "./db/img/" + get_file_name(uploaded_file)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO analysis 
                   (image_path, has_person, has_hardhat, employee_name) 
            VALUES (?, ?, ?, ?)""",
            (file_path, has_person, has_hardhat, employee_name),
        )
        conn.commit()

    st.session_state["selected_row"] = None


def render_result(model: YOLO, uploaded_file: UploadedFile) -> None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    results = model(image)

    has_person = False
    has_hardhat = False

    for r in results:
        for c in r.boxes.cls:
            if model.names[int(c)] == "person":
                has_person = True
            if model.names[int(c)] == "hardhat":
                has_hardhat = True

    st.subheader("Resultado da Análise:")

    if has_person and not has_hardhat:
        st.error("ACESSO NEGADO: Pessoa sem capacete detectada.")
    elif has_person and has_hardhat:
        st.success("ACESSO LIBERADO: Pessoa com capacete detectada.")
    elif not has_person and has_hardhat:
        st.success("ACESSO LIBERADO: Somente capacete detectado.")
    else:
        st.warning("Nenhuma pessoa ou capacete detectado.")

    for r in results:
        im_array = r.plot()
        im = Image.fromarray(im_array[..., ::-1])

    st.image(im, caption="Imagem com as detecções", width="stretch")

    col1, col2, col3 = st.columns([4, 2, 4], vertical_alignment="bottom")

    with col1:
        employee_name = st.text_input("Nome da pessoa", value="Não identificado")

    with col2:
        button = st.button(
            "Salvar Análise",
            on_click=save_analysis,
            args=(uploaded_file, has_person, has_hardhat, employee_name),
        )

    with col3:
        if button:
            st.success(":white_check_mark: Salvo com sucesso.")


def render_analysis() -> None:
    model = load_model()
    if model is None:
        st.error("Modelo não carregado.")
        return

    st.title("Análise de Imagem")
    st.info(":information_source: Selecione uma imagem para análise no campo abaixo.")

    uploaded_file = st.file_uploader("Carregue uma imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is None:
        st.warning("Nenhuma imagem carregada.")
        return

    render_result(model, uploaded_file)
