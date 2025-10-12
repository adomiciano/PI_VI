import streamlit as st
from modules.common import render_menu, render_home
from modules.analisis import render_analysis
from modules.history import render_history


def main():
    st.set_page_config(
        page_title="Identificação de EPI", page_icon=":guardsman", layout="wide"
    )

    page = st.navigation(
        [
            st.Page(render_home, title="Home"),
            st.Page(render_analysis, title="Análise de Imagem"),
            st.Page(render_history, title="Histórico de Análises"),
        ], position="sidebar"
    )
    page.run()

    # option = render_menu()

    # match option:
    #     case "Home":
    #         render_home()
    #     case "Análise de Imagem":
    #         render_analysis()
    #     case "Histórico de Análises":
    #         render_history()


if __name__ == "__main__":
    main()
