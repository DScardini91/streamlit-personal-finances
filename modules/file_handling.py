import streamlit as st
import pandas as pd

def upload_json():
    return


def save_data(file_name):
    file_name = f"{file_name}.parquet" if not file_name.endswith(".parquet") else file_name
    st.session_state.df.to_parquet(file_name)
    st.success(f"Dados salvos em {file_name}")

def load_data(uploaded_file):
    st.session_state.df = pd.read_parquet(uploaded_file)
    st.success("Dados carregados com sucesso")
