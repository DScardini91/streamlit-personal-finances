import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_processing import calculate_balance


# Função para carregar o balance_df
def load_balance():
    if "balance_df" in st.session_state and not st.session_state.balance_df.empty:
        return st.session_state.balance_df
    else:
        if "df" in st.session_state and not st.session_state.df.empty:
            balance_df, _ = calculate_balance(
                st.session_state.df, "06/01/2024", "31/12/2024"
            )
            st.session_state.balance_df = balance_df
            return balance_df
        else:
            st.error("Nenhum dado de transação disponível para calcular o balanço.")
            return pd.DataFrame(
                columns=[
                    "Data",
                    "Saldo Inicial",
                    "Valor Previsto de Transações",
                    "Saldo Previsto",
                ]
            )


def display_balance():
    balance_df = load_balance()
    today = datetime.today().strftime("%d/%m/%Y")

    if today not in balance_df["Data"].values:
        saldo_atual = 0.0
        transacoes_hoje = 0.0
    else:
        saldo_atual = balance_df.loc[
            balance_df["Data"] == today, "Saldo Previsto"
        ].values[0]
        transacoes_hoje = balance_df.loc[
            balance_df["Data"] == today, "Valor Previsto de Transações"
        ].values[0]

    return saldo_atual, transacoes_hoje


def home():
    st.subheader("Home")

    # Inicializa st.session_state se não existir
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            columns=[
                "Tipo",
                "Categoria",
                "Classe",
                "Origem",
                "Descrição",
                "Valor",
                "Observação",
                "Data",
                "MesAno",
                "Inclusão",
                "Realizado",
            ]
        )
    if "balance_df" not in st.session_state:
        st.session_state.balance_df = pd.DataFrame(
            columns=[
                "Data",
                "Saldo Inicial",
                "Valor Previsto de Transações",
                "Saldo Previsto",
            ]
        )

    saldo_atual, transacoes_hoje = display_balance()

    col1, col2 = st.columns([2, 1])  # Coluna 1: 66%, Coluna 2: 33%

    # Card para o saldo atual
    with col1:
        st.markdown(
            f"""
            <div style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #f8f9fa;">
                <h4 style="color: #6c757d; margin: 0;">Saldo Atual</h4>
                <p style="color: {'#155724' if saldo_atual >= 0 else '#721c24'}; font-size: 24px; margin: 0;">R${saldo_atual:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Card para transações previstas para hoje
    with col2:
        st.markdown(
            f"""
            <div style="border: 1px solid #e1e4e8; border-radius: 6px; padding: 16px; background-color: #f8f9fa;">
                <h4 style="color: #6c757d; margin: 0;">Transações Previstas para Hoje</h4>
                <p style="color: {'#155724' if transacoes_hoje >= 0 else '#721c24'}; font-size: 24px; margin: 0;">R${transacoes_hoje:,.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    home()
