import streamlit as st
import pandas as pd
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from modules.options_handler import load_options

options = load_options()


# Inicializa um DataFrame vazio se não existir
def initialize_df():
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(
            columns=[
                "Tipo",
                "Categoria",
                "Classe",
                "Subclasse",
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
    else:
        # Garante que a coluna 'Subclasse' esteja presente
        if "Subclasse" not in st.session_state.df.columns:
            st.session_state.df["Subclasse"] = ""


# Inicializa inputs vazios
def initialize_inputs():
    st.session_state.inputs = {
        "tipo": "Gasto",
        "categoria": "Custos Fixos",
        "classe": "",
        "subclasse": "",
        "origem": "",
        "descricao": "",
        "valor": "0,00",
        "observacao": "",
        "data_transacao": datetime.today().strftime("%d/%m/%Y"),
        "realizado": False,
        "recorrente": False,
        "periodicidade": 1,
        "duracao": 1,
    }


def parse_date(date_str):
    if isinstance(date_str, str) and date_str:
        return datetime.strptime(date_str, "%d/%m/%Y").date()
    return datetime.today().date()


def format_date(date_obj):
    if isinstance(date_obj, date):
        return date_obj.strftime("%d/%m/%Y")
    return date_obj


def ensure_date_format():
    if "df" in st.session_state and not st.session_state.df.empty:
        st.session_state.df["Data"] = pd.to_datetime(
            st.session_state.df["Data"], dayfirst=True
        ).dt.strftime("%d/%m/%Y")


# Adicione a chamada para a função ensure_date_format onde necessário
def manual_entry():
    # Carrega as opções do session_state
    options = load_options()
    st.subheader("Adicionar transação")

    initialize_df()
    ensure_date_format()
    if "inputs" not in st.session_state:
        initialize_inputs()

    tipos = options["tipo_options"]
    categorias = options["categoria_options"].get(st.session_state.inputs["tipo"], [])
    classes = options["classe_options"].get(st.session_state.inputs["categoria"], [])
    subclasses = options["subclasse_options"].get(st.session_state.inputs["classe"], [])
    origens = options["origem_options"].get(st.session_state.inputs["tipo"], [])

    col1, col2 = st.columns([1, 2])

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
        subclasses = options["subclasse_options"].get(
            st.session_state.inputs["classe"], []
        )
        st.session_state.inputs["subclasse"] = st.selectbox(
            "Subclasse",
            subclasses,
            index=(
                subclasses.index(st.session_state.inputs["subclasse"])
                if st.session_state.inputs["subclasse"] in subclasses
                else 0
            ),
        )
        origens = options["origem_options"].get(st.session_state.inputs["tipo"], [])
        st.session_state.inputs["origem"] = st.selectbox(
            "Origem",
            origens,
            index=(
                origens.index(st.session_state.inputs["origem"])
                if st.session_state.inputs["origem"] in origens
                else 0
            ),
        )

        st.session_state.inputs["descricao"] = st.text_input(
            "Descrição", st.session_state.inputs["descricao"]
        )

        valor_input = st.text_input("Valor (R$)", st.session_state.inputs["valor"])
        # Permite ponto ou vírgula para decimais
        if not valor_input.replace(".", "", 1).replace(",", "", 1).isdigit():
            st.warning("Por favor, insira apenas números no campo Valor.")
        else:
            # Substitui vírgula por ponto para garantir consistência no formato decimal
            st.session_state.inputs["valor"] = valor_input.replace(",", ".")

        st.session_state.inputs["observacao"] = st.text_input(
            "Observação", st.session_state.inputs["observacao"]
        )
        data_transacao = parse_date(st.session_state.inputs["data_transacao"])
        st.session_state.inputs["data_transacao"] = st.date_input(
            "Data da Transação",
            value=data_transacao if data_transacao else datetime.today().date(),
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

    if confirm_button:
        if not valor_input.replace(".", "", 1).replace(",", "", 1).isdigit():
            st.warning("Por favor, insira um valor numérico válido.")
        else:
            valor = float(st.session_state.inputs["valor"])
            data_hora_inclusao = datetime.now()

            # Verificar se a transação já existe
            transacao_existente = st.session_state.df[
                (st.session_state.df["Tipo"] == st.session_state.inputs["tipo"])
                & (
                    st.session_state.df["Categoria"]
                    == st.session_state.inputs["categoria"]
                )
                & (st.session_state.df["Classe"] == st.session_state.inputs["classe"])
                & (
                    st.session_state.df["Subclasse"]
                    == st.session_state.inputs["subclasse"]
                )
                & (st.session_state.df["Origem"] == st.session_state.inputs["origem"])
                & (
                    st.session_state.df["Descrição"]
                    == st.session_state.inputs["descricao"]
                )
                & (st.session_state.df["Valor"] == valor)
                & (
                    st.session_state.df["Observação"]
                    == st.session_state.inputs["observacao"]
                )
                & (
                    st.session_state.df["Data"]
                    == st.session_state.inputs["data_transacao"].strftime("%d/%m/%Y")
                )
            ]

            if st.session_state.inputs["recorrente"] and transacao_existente.empty:
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
                            "Subclasse": [st.session_state.inputs["subclasse"]],
                            "Origem": [st.session_state.inputs["origem"]],
                            "Descrição": [st.session_state.inputs["descricao"]],
                            "Valor": [valor],
                            "Observação": [st.session_state.inputs["observacao"]],
                            "Data": [data_transacao.strftime("%d/%m/%Y")],
                            "MesAno": [mes_ano],
                            "Inclusão": [data_hora_inclusao],
                            "Realizado": [False],
                        }
                    )
                    st.session_state.df = pd.concat(
                        [st.session_state.df, new_transaction], ignore_index=True
                    )
                    st.success(
                        f"Transação recorrente adicionada com sucesso! Foram adicionadas {st.session_state.inputs['duracao'] // st.session_state.inputs['periodicidade']} recorrências, no valor total de R$ {st.session_state.inputs['valor'] * (st.session_state.inputs['duracao'] // st.session_state.inputs['periodicidade'])}"
                    )
            elif transacao_existente.empty:
                data_transacao = st.session_state.inputs["data_transacao"]
                mes_ano = data_transacao.strftime("%m/%Y")
                new_transaction = pd.DataFrame(
                    {
                        "Tipo": [st.session_state.inputs["tipo"]],
                        "Categoria": [st.session_state.inputs["categoria"]],
                        "Classe": [st.session_state.inputs["classe"]],
                        "Subclasse": [st.session_state.inputs["subclasse"]],
                        "Origem": [st.session_state.inputs["origem"]],
                        "Descrição": [st.session_state.inputs["descricao"]],
                        "Valor": [valor],
                        "Observação": [st.session_state.inputs["observacao"]],
                        "Data": [data_transacao.strftime("%d/%m/%Y")],
                        "MesAno": [mes_ano],
                        "Inclusão": [data_hora_inclusao],
                        "Realizado": [st.session_state.inputs["realizado"]],
                    }
                )
                st.session_state.df = pd.concat(
                    [st.session_state.df, new_transaction], ignore_index=True
                )
                st.success(
                    f"Transação adicionada com sucesso! Valor: R$ {valor}, Data: {data_transacao.strftime('%d/%m/%Y')}"
                )

            else:
                st.warning("Já existe uma transação idêntica lançada.")
                print("Transação já existente. Não foi adicionada.")

            initialize_inputs()
            st.rerun()
            ensure_date_format()

    with col2:
        st.write("Transações Registradas:")

        ensure_date_format()
        if not st.session_state.df.empty:
            st.session_state.df = st.session_state.df.sort_values(
                by="Inclusão", ascending=False
            )
            st.dataframe(
                st.session_state.df.drop(columns=["Inclusão"]).reset_index(drop=True)
            )


if __name__ == "__main__":
    manual_entry()
