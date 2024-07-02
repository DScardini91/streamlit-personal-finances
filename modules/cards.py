import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_processing import calculate_card_statements, load_card_data


# Função para carregar as faturas dos cartões com configuração constante
def card_statements_view():
    st.subheader("Faturas dos Cartões")

    if "df" not in st.session_state or st.session_state.df.empty:
        st.write("Nenhum dado de transação disponível.")
        return

    # Configurações constantes dos cartões
    card_data = pd.DataFrame(
        {
            "Cartão": ["Elo", "Mastercard", "Visa"],
            "Dia de Pagamento": [25, 25, 11],
            "Dia de Fechamento": [12, 12, 27],
        }
    )

    card_statements = calculate_card_statements(st.session_state.df, card_data)

    if len(card_statements) == 0:
        st.warning("Nenhuma fatura de cartão disponível. Cadastre novas transações")

    for statement in card_statements:
        st.markdown(f"### Fatura do Cartão {statement['Cartão']}")
        st.markdown(f"**Fechamento:** {statement['Fechamento'].strftime('%d/%m/%Y')}")
        st.markdown(f"**Pagamento:** {statement['Pagamento'].strftime('%d/%m/%Y')}")
        st.markdown(f"**Total:** R${statement['Total']:.2f}")

        st.dataframe(statement["Transações"])


if __name__ == "__main__":
    card_statements_view()
