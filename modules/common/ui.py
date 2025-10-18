import streamlit as st


def render_menu() -> str:
    st.sidebar.title("Menu de Opções")

    return st.sidebar.selectbox(
        "Selecione uma opção",
        ["Home", "Análise de Imagem", "Histórico de Análises"]
    )


def render_home():
    st.title(":guardsman: Sistema de identificação de EPI")

    st.markdown("""
    Bem-vindo ao sistema de identificação de EPI.
    
    Essa aplicação foi desenvolvida para identificar pessoas com EPI em imagens de câmeras de segurança.
    
    A aplicação foi desenvolvida no **Projeto Integrador 6** da UNIVESP - Universidade Virtual do Estado de São Paulo.
    """)

    st.info(":information_source: Selecione uma opção no menu lateral para continuar.")
