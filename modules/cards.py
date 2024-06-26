import streamlit as st
import pandas as pd
import os
from modules.data_processing import calculate_card_statements, load_card_data


# Função para carregar os dados dos cartões de um arquivo parquet
def load_card_data():
    if os.path.exists("cards.parquet"):
        return pd.read_parquet("cards.parquet")
    else:
        return pd.DataFrame(columns=["Cartão", "Dia de Pagamento", "Dia de Fechamento"])


# Função para salvar os dados dos cartões em um arquivo parquet
def save_card_data(df):
    df.to_parquet("cards.parquet")


def card_management():
    st.subheader("Cadastro de Cartões")

    card_df = load_card_data()

    col1, col2 = st.columns(2)

    with col1:
        # Lista de cartões para gerenciar
        cards = ["Visa", "Elo", "Mastercard"]

        # Exibir os campos de edição para cada cartão
        for card in cards:
            st.write(f"### {card}")

            # Carregar os dias existentes ou definir valores padrão
            if card in card_df["Cartão"].values:
                card_data = card_df[card_df["Cartão"] == card].iloc[0]
                payment_day = card_data["Dia de Pagamento"]
                closing_day = card_data["Dia de Fechamento"]
            else:
                payment_day = 1
                closing_day = 1

            # Campos para editar os dias
            payment_day = st.slider(f"Dia de Pagamento ({card})", 1, 30, payment_day)
            closing_day = st.slider(f"Dia de Fechamento ({card})", 1, 30, closing_day)

            # Atualizar os dados no DataFrame
            if card in card_df["Cartão"].values:
                card_df.loc[card_df["Cartão"] == card, "Dia de Pagamento"] = payment_day
                card_df.loc[card_df["Cartão"] == card, "Dia de Fechamento"] = (
                    closing_day
                )
            else:
                new_row = pd.DataFrame(
                    {
                        "Cartão": [card],
                        "Dia de Pagamento": [payment_day],
                        "Dia de Fechamento": [closing_day],
                    }
                )
                card_df = pd.concat([card_df, new_row], ignore_index=True)

        # Botão para salvar os dados
        if st.button("Salvar Dados de Cartões"):
            save_card_data(card_df)
            st.success("Dados de cartões salvos com sucesso!")

    with col2:
        # Exibir os dados dos cartões
        st.write("### Dados dos Cartões")
        st.dataframe(card_df)

        # Exibir as faturas dos cartões
        st.write("### Faturas dos Cartões")
        df = st.session_state.df.copy() if "df" in st.session_state else pd.DataFrame()
        if not df.empty:
            card_statements = calculate_card_statements(df, card_df)
            for statement in card_statements:
                st.write(f"#### Fatura do Cartão: {statement['Cartão']}")
                st.write(f"Fechamento: {statement['Fechamento'].strftime('%d/%m/%Y')}")
                st.write(f"Pagamento: {statement['Pagamento'].strftime('%d/%m/%Y')}")
                st.write(f"Total: R${statement['Total']:.2f}")
                st.dataframe(statement["Transações"][["Data", "Descrição", "Valor"]])


if __name__ == "__main__":
    card_management()
