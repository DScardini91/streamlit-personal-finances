import streamlit as st
import pandas as pd
import json


# Função para carregar opções do arquivo JSON
def load_options():
    with open("modules/options.json", "r") as f:
        options = json.load(f)
    return options


options = load_options()


def apply_styles(df):
    def color_rows(row):
        color = "background-color: "
        if row["Tipo"] == "Receita":
            color += "rgba(0, 255, 0, 0.1)"
        elif row["Tipo"] == "Gasto":
            color += "rgba(255, 0, 0, 0.1)"
        else:
            color += "white"
        return [color] * len(row)

    return df.style.apply(color_rows, axis=1)


def view_data():
    st.subheader("Visualização dos dados")

    if "df" not in st.session_state or st.session_state.df.empty:
        st.write("Nenhum dado disponível. Carregue os dados para visualizar.")
        return

    df = st.session_state.df.copy()

    st.write("Transações Filtradas:")

    # Configuração do DataFrame editável com dropdowns
    edited_df = st.data_editor(
        df.drop(columns=["Inclusão"]),
        num_rows="dynamic",
        column_config={
            "Tipo": {"options": options["tipo_options"]},
            "Categoria": {"options": sum(options["categoria_options"].values(), [])},
            "Classe": {"options": sum(options["classe_options"].values(), [])},
            "Descrição": {},
            "Observação": {},
            "Valor": {"format": "R$%.2f"},
            "Realizado": {"options": [True, False]},
        },
    )

    st.session_state.df.update(edited_df)

    # styled_df = apply_styles(st.session_state.df)
    # st.write(styled_df.to_html(), unsafe_allow_html=True)


def show_dashboard():
    return


if __name__ == "__main__":
    view_data()
