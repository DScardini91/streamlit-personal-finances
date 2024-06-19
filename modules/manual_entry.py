import streamlit as st
import pandas as pd
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta


# Função para carregar opções do arquivo JSON
def load_options():
    with open("modules/options.json", "r") as f:
        options = json.load(f)
    return options


options = load_options()


# Inicializa um DataFrame vazio se não existir
def initialize_df():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            columns=[
                "Tipo",
                "Categoria",
                "Classe",
                "Descrição",
                "Valor",
                "Observação",
                "Data",
                "MesAno",
                "Inclusão",
                "Realizado",
            ]
        )


def initialize_inputs():
    if "inputs" not in st.session_state:
        st.session_state.inputs = {
            "tipo": "Gasto",
            "categoria": "Custos fixos",
            "classe": "",
            "descricao": "",
            "valor": 0.00,
            "observacao": "",
            "data_transacao": datetime.today(),
            "realizado": False,
            "recorrente": False,
            "periodicidade": 1,
            "duracao": 1,
        }


def manual_entry():
    st.subheader("Adicionar transação")

    initialize_df()
    initialize_inputs()

    tipos = options["tipo_options"]
    categorias = options["categoria_options"].get(st.session_state.inputs["tipo"], [])
    classes = options["classe_options"].get(st.session_state.inputs["categoria"], [])

    col1, col2 = st.columns(2)

    with col1:
        st.session_state.inputs["tipo"] = st.selectbox(
            "Tipo", tipos, index=tipos.index(st.session_state.inputs["tipo"])
        )
        categorias = options["categoria_options"].get(
            st.session_state.inputs["tipo"], []
        )
        st.session_state.inputs["categoria"] = st.selectbox(
            "Categoria",
            categorias,
            index=(
                categorias.index(st.session_state.inputs["categoria"])
                if st.session_state.inputs["categoria"] in categorias
                else 0
            ),
        )
        classes = options["classe_options"].get(
            st.session_state.inputs["categoria"], []
        )
        st.session_state.inputs["classe"] = st.selectbox(
            "Classe",
            classes,
            index=(
                classes.index(st.session_state.inputs["classe"])
                if st.session_state.inputs["classe"] in classes
                else 0
            ),
        )

        st.session_state.inputs["descricao"] = st.text_input(
            "Descrição", st.session_state.inputs["descricao"]
        )
        st.session_state.inputs["valor"] = st.number_input(
            "Valor (R$)",
            min_value=0.00,
            format="%.2f",
            value=st.session_state.inputs["valor"],
        )
        st.session_state.inputs["observacao"] = st.text_input(
            "Observação", st.session_state.inputs["observacao"]
        )
        st.session_state.inputs["data_transacao"] = st.date_input(
            "Data da Transação", value=st.session_state.inputs["data_transacao"]
        )
        st.session_state.inputs["realizado"] = st.checkbox(
            "Realizado", value=st.session_state.inputs.get("realizado", False)
        )
        st.session_state.inputs["recorrente"] = st.checkbox(
            "Transação Recorrente",
            value=st.session_state.inputs.get("recorrente", False),
        )

        if st.session_state.inputs["recorrente"]:
            st.session_state.inputs["periodicidade"] = st.number_input(
                "Periodicidade (em meses)",
                min_value=1,
                step=1,
                value=st.session_state.inputs["periodicidade"],
            )
            st.session_state.inputs["duracao"] = st.number_input(
                "Duração (em meses)",
                min_value=1,
                step=1,
                value=st.session_state.inputs["duracao"],
            )

        confirm_button = st.button(label="✅ Confirmar")
        correct_button = st.button(label="🧽 Corrigir")

    if confirm_button:
        data_hora_inclusao = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if st.session_state.inputs["recorrente"]:
            for i in range(
                0,
                st.session_state.inputs["duracao"],
                st.session_state.inputs["periodicidade"],
            ):
                data_transacao = st.session_state.inputs[
                    "data_transacao"
                ] + relativedelta(months=i)
                mes_ano = data_transacao.strftime("%m/%Y")
                new_transaction = pd.DataFrame(
                    {
                        "Tipo": [st.session_state.inputs["tipo"]],
                        "Categoria": [st.session_state.inputs["categoria"]],
                        "Classe": [st.session_state.inputs["classe"]],
                        "Descrição": [st.session_state.inputs["descricao"]],
                        "Valor": [st.session_state.inputs["valor"]],
                        "Observação": [st.session_state.inputs["observacao"]],
                        "Data": [data_transacao.strftime("%d/%m/%Y")],
                        "MesAno": [mes_ano],
                        "Inclusão": [data_hora_inclusao],
                        "Realizado": [
                            False
                        ],  # Sempre False para transações recorrentes
                    }
                )
                st.session_state.df = pd.concat(
                    [st.session_state.df, new_transaction], ignore_index=True
                )
        else:
            mes_ano = st.session_state.inputs["data_transacao"].strftime("%m/%Y")
            new_transaction = pd.DataFrame(
                {
                    "Tipo": [st.session_state.inputs["tipo"]],
                    "Categoria": [st.session_state.inputs["categoria"]],
                    "Classe": [st.session_state.inputs["classe"]],
                    "Descrição": [st.session_state.inputs["descricao"]],
                    "Valor": [st.session_state.inputs["valor"]],
                    "Observação": [st.session_state.inputs["observacao"]],
                    "Data": [
                        st.session_state.inputs["data_transacao"].strftime("%d/%m/%Y")
                    ],
                    "MesAno": [mes_ano],
                    "Inclusão": [data_hora_inclusao],
                    "Realizado": [st.session_state.inputs["realizado"]],
                }
            )
            st.session_state.df = pd.concat(
                [st.session_state.df, new_transaction], ignore_index=True
            )

        st.success(
            f"Adicionado: {st.session_state.inputs['descricao']} de valor R${st.session_state.inputs['valor']:.2f} como {st.session_state.inputs['tipo']} em {st.session_state.inputs['data_transacao'].strftime('%d/%m/%Y')}"
        )

    if correct_button:
        initialize_inputs()
        st.warning("Corrigir entrada. Por favor, preencha novamente os campos.")

    with col2:
        st.write("Transações Registradas:")
        if not st.session_state.df.empty:
            st.session_state.df = st.session_state.df.sort_values(
                by="Inclusão", ascending=False
            )
            st.dataframe(
                st.session_state.df.drop(columns=["Inclusão"]).reset_index(drop=True)
            )
