import streamlit as st
import pandas as pd
import json
from datetime import datetime, date


def save_data(file_name):
    def convert_timestamps(data):
        for key, value in data.items():
            if isinstance(value, dict):
                convert_timestamps(value)
            elif isinstance(value, (pd.Timestamp, datetime, date)):
                data[key] = value.isoformat()

    data = {
        "transactions": st.session_state.df.to_dict(),
        "balance": (
            st.session_state.balance_df.to_dict()
            if "balance_df" in st.session_state
            else {}
        ),
        "cards": (
            st.session_state.cards_df.to_dict()
            if "cards_df" in st.session_state
            else {}
        ),
    }

    # Convert timestamps to ISO format strings
    convert_timestamps(data)

    with open(file_name, "w") as f:
        json.dump(data, f)
    st.session_state.saved_file_name = file_name
    st.success(f"Dados salvos em {file_name}")


def save_data_as():
    file_name = st.text_input("Digite o nome do arquivo (sem extensão):", key="save_as")
    if st.button("Salvar", key="save_as_button"):
        if file_name:
            save_data(file_name + ".json")
        else:
            st.warning("Por favor, insira um nome de arquivo.")


def load_data(uploaded_file):
    def convert_strings_to_timestamps(data):
        for key, value in data.items():
            if isinstance(value, dict):
                convert_strings_to_timestamps(value)
            elif isinstance(value, str):
                try:
                    data[key] = pd.to_datetime(value)
                except ValueError:
                    pass

    data = json.load(uploaded_file)
    convert_strings_to_timestamps(data)

    st.session_state.df = pd.DataFrame(data["transactions"])
    for column in ["Descrição", "Categoria", "Classe", "Origem"]:
        if column in st.session_state.df:
            st.session_state.df[column] = st.session_state.df[column].astype(str)

    if "balance" in data:
        st.session_state.balance_df = pd.DataFrame(data["balance"])
    if "cards" in data:
        st.session_state.cards_df = pd.DataFrame(data["cards"])
    st.success("Dados carregados com sucesso")


def download_data():
    if "saved_file_name" in st.session_state:
        with open(st.session_state.saved_file_name, "rb") as f:
            st.download_button(
                label="Download Dados",
                data=f,
                file_name=st.session_state.saved_file_name,
                mime="application/json",
            )
    else:
        st.warning("Salve os dados antes de baixar.")
