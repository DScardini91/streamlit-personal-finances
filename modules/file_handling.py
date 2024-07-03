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
        "goals": (st.session_state.goals if "goals" in st.session_state else {}),
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

    def clean_currency(value):
        if isinstance(value, str):
            return value.replace("R$", "").replace(",", "").strip()
        return value

    def ensure_correct_format(df):
        if "Data" in df.columns:
            df["Data"] = pd.to_datetime(df["Data"], errors="coerce").dt.strftime(
                "%d/%m/%Y"
            )
        if "MesAno" in df.columns:
            df["MesAno"] = pd.to_datetime(
                df["MesAno"], errors="coerce", format="%m/%Y"
            ).dt.strftime("%m/%Y")
        for col in ["Descrição", "Categoria", "Classe", "Origem", "Observação"]:
            if col in df.columns:
                df[col] = df[col].fillna("").astype(str)
        if "Valor" in df.columns:
            df["Valor"] = df["Valor"].apply(clean_currency).astype(float)
        if "Realizado" in df.columns:
            df["Realizado"] = df["Realizado"].astype(bool)
        if "Saldo Inicial" in df.columns:
            df["Saldo Inicial"] = (
                df["Saldo Inicial"].apply(clean_currency).astype(float)
            )
        if "Valor Previsto de Transações" in df.columns:
            df["Valor Previsto de Transações"] = (
                df["Valor Previsto de Transações"].apply(clean_currency).astype(float)
            )
        if "Saldo Previsto" in df.columns:
            df["Saldo Previsto"] = (
                df["Saldo Previsto"].apply(clean_currency).astype(float)
            )
        return df

    data = json.load(uploaded_file)
    convert_strings_to_timestamps(data)

    st.session_state.df = pd.DataFrame(data["transactions"])
    st.session_state.df = ensure_correct_format(st.session_state.df)

    if "balance" in data:
        st.session_state.balance_df = pd.DataFrame(data["balance"])
        st.session_state.balance_df = ensure_correct_format(st.session_state.balance_df)
    if "cards" in data:
        st.session_state.cards_df = pd.DataFrame(data["cards"])
    if "goals" in data:
        st.session_state.goals = data["goals"]
    else:
        st.session_state.goals = {
            "Custos fixos": 60,
            "Prazeres": 10,
            "Conforto": 15,
            "Conhecimento": 5,
            "Liberdade Financeira": 10,
            "Dízimo": 10,
            "Reembolsável": 0,
        }
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
