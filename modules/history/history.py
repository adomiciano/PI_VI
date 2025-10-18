import streamlit as st
from modules.history import create_connection
import pandas as pd


DISPLAY_COLUMNS = ["Nome", "Data", "Pessoa na Imagem", "Capacete na Imagem", "Imagem"]
RENDER_COLUMNS = ["Nome", "Data", "Pessoa na Imagem", "Capacete na Imagem", "Seleção"]


def adjust_df(df):
    df["created_at"] = pd.to_datetime(df["created_at"])

    df.rename(
        columns={
            "image_path": "Imagem",
            "created_at": "Data",
            "has_person": "Pessoa na Imagem",
            "has_hardhat": "Capacete na Imagem",
            "employee_name": "Nome",
        },
        inplace=True,
    )

    df["Pessoa na Imagem"] = df["Pessoa na Imagem"].apply(
        lambda x: "Sim" if x else "Não"
    )

    df["Capacete na Imagem"] = df["Capacete na Imagem"].apply(
        lambda x: "Sim" if x else "Não"
    )

    df.drop(columns=["id"], inplace=True)
    df.sort_values(by="Data", inplace=True)

    df = df[DISPLAY_COLUMNS]

    return df


def render_image(row: pd.Series):
    st.session_state["selected_row"] = row


def render_table(df):
    columns = st.columns(len(RENDER_COLUMNS), vertical_alignment="center", border=True)

    for col, column_name in zip(columns, RENDER_COLUMNS):
        with col:
            with st.container(
                border=False,
                height=50,
                horizontal_alignment="center",
                vertical_alignment="center",
            ):
                st.markdown(
                    f"<p style='text-align: center;font-size: 20px;'><strong>{column_name}</strong></p>",
                    unsafe_allow_html=True,
                )

    data_columns = st.columns(
        len(RENDER_COLUMNS), vertical_alignment="top", border=False
    )

    for id, row in df.iterrows():
        for col, column_name in zip(data_columns, RENDER_COLUMNS):
            with col:
                with st.container(
                    border=True,
                    height=60,
                    horizontal_alignment="center",
                    vertical_alignment="center",
                ):
                    if column_name == "Seleção":
                        st.button(
                            "Selecionar",
                            key=id,
                            use_container_width=True,
                            type="primary",
                            on_click=render_image,
                            args=(row,)
                        )
                        continue

                    st.markdown(
                        f"<p style='text-align: center;'>{row[column_name]}</p>",
                        unsafe_allow_html=True,
                    )


def render_history():

    with create_connection() as conn:
        df = pd.read_sql_query(
            """
        SELECT
            id,
            image_path,
            datetime(created_at, 'localtime') AS created_at,
            has_person,
            has_hardhat,
            employee_name
        FROM analysis
        """,
            conn,
        )

        if st.session_state.get("selected_row") is not None:
            selected_row = st.session_state["selected_row"]
            st.subheader(":mag: Registro selecionado")

            row_columns = st.columns(len(RENDER_COLUMNS) - 1)

            for col, column_name in zip(row_columns, RENDER_COLUMNS):
                with col:
                    st.markdown(f"**{column_name}**: {selected_row[column_name]}")

                        
            st.image(selected_row["Imagem"])

        st.subheader(":floppy_disk: Histórico de Análises")
        render_table(adjust_df(df))
