import streamlit as st
import pandas as pd


def save_data(file_name):
    file_name = (
        f"{file_name}.parquet" if not file_name.endswith(".parquet") else file_name
    )
    st.session_state.df.to_parquet(file_name)
    st.session_state.saved_file_name = file_name
    st.success(f"Dados salvos em {file_name}")


def save_data_as():
    file_name = st.text_input("Digite o nome do arquivo (sem extensão):", key="save_as")
    if st.button("Salvar", key="save_as_button"):
        if file_name:
            save_data(file_name)
        else:
            st.warning("Por favor, insira um nome de arquivo.")


def load_data(uploaded_file):
    st.session_state.df = pd.read_parquet(uploaded_file)
    st.success("Dados carregados com sucesso")


def download_data():
    if "saved_file_name" in st.session_state:
        with open(st.session_state.saved_file_name, "rb") as f:
            st.download_button(
                label="Download Dados",
                data=f,
                file_name=st.session_state.saved_file_name,
                mime="application/octet-stream",
            )
    else:
        st.warning("Salve os dados antes de baixar.")
