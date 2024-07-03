import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


# Função para gerar alertas de saldo negativo
def generate_alerts(balance_df):
    today = datetime.today().date()
    next_15_days = today + timedelta(days=15)
    current_month = today.strftime("%m/%Y")

    balance_df["Data"] = pd.to_datetime(balance_df["Data"], format="%d/%m/%Y").dt.date
    balance_df["Saldo Previsto"] = (
        balance_df["Saldo Previsto"]
        .astype(str)
        .str.replace("R$", "")
        .str.replace(",", "")
        .astype(float)
    )

    alerts = balance_df[
        (balance_df["Data"] >= today)
        & (balance_df["Data"] <= next_15_days)
        & (balance_df["Saldo Previsto"] < 0)
    ]

    return alerts


def display_alerts():
    if "balance_df" not in st.session_state or st.session_state.balance_df.empty:
        st.write("Nenhum dado de balanço disponível para gerar alertas.")
        return

    alerts = generate_alerts(st.session_state.balance_df)

    if not alerts.empty:
        st.warning("Alertas de Saldo Negativo nos Próximos 15 Dias")
        for _, row in alerts.iterrows():
            st.warning(
                f"Dia {row['Data'].strftime('%d/%m/%Y')}: Saldo Previsto Negativo de R${row['Saldo Previsto']:.2f}"
            )
    else:
        st.info("Nenhum alerta de saldo negativo nos próximos 15 dias.")
