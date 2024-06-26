import streamlit as st
import pandas as pd
import json
from datetime import datetime
from modules.data_processing import calculate_balance


# Função para carregar opções do arquivo JSON
def load_options():
    with open("modules/options.json", "r") as f:
        options = json.load(f)
    return options


options = load_options()


def apply_balance_styles(df):
    def color_transactions(val):
        if isinstance(val, str):
            val = float(val.replace("R$", "").replace(",", ""))
        color = ""
        if val > 0:
            color += "background-color: rgba(0, 255, 0, 0.1);"
        elif val < 0:
            color += "background-color: rgba(255, 0, 0, 0.1);"
        return color

    def color_balance(val):
        if isinstance(val, str):
            val = float(val.replace("R$", "").replace(",", ""))
        if val < 0:
            return "background-color: rgba(255, 0, 0, 0.7); color: white; font-weight: bold;"
        elif val > 0:
            return "background-color: rgba(0, 255, 0, 0.1);"
        else:
            return ""  # Sem preenchimento para saldo zero

    styled_df = df.style.applymap(
        color_transactions, subset=["Valor Previsto de Transações"]
    ).applymap(color_balance, subset=["Saldo Previsto"])
    return styled_df


def view_data():
    st.subheader("Visualização das Transações")

    if "df" not in st.session_state or st.session_state.df.empty:
        st.write("Nenhum dado disponível. Carregue os dados para visualizar.")
        return

    df = st.session_state.df.copy()

    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.strftime("%d/%m/%Y")
    df["MesAno"] = pd.to_datetime(df["MesAno"], format="%m/%Y").dt.strftime("%Y/%m")

    tipos = st.multiselect(
        "Tipo",
        options=options["tipo_options"],
    )
    categorias = st.multiselect(
        "Categoria",
        options=sum(options["categoria_options"].values(), []),
    )
    classes = st.multiselect(
        "Classe",
        options=sum(options["classe_options"].values(), []),
    )
    origens = st.multiselect(
        "Origem",
        options=options["origem_options"]["Gasto"],
    )
    meses = st.multiselect("Mês/Ano", options=sorted(df["MesAno"].unique().tolist()))
    data_inicial = st.date_input("Data de inclusão maior que", value=None)

    if tipos:
        df = df[df["Tipo"].isin(tipos)]
    if categorias:
        df = df[df["Categoria"].isin(categorias)]
    if classes:
        df = df[df["Classe"].isin(classes)]
    if origens:
        df = df[df["Origem"].isin(origens)]
    if meses:
        df = df[df["MesAno"].isin(meses)]
    if data_inicial:
        df["Inclusão"] = pd.to_datetime(
            df["Inclusão"], format="%d/%m/%Y %H:%M:%S", errors="coerce"
        )
        df = df[df["Inclusão"] > pd.to_datetime(data_inicial)]

    st.write("Transações Filtradas:")
    st.dataframe(df)


def view_balance():
    st.subheader("Balanço Financeiro dos Dias")

    if "df" not in st.session_state or st.session_state.df.empty:
        st.write("Nenhum dado disponível. Carregue os dados para visualizar.")
        return

    balance_df, card_statements = calculate_balance(
        st.session_state.df, "06/01/2024", "12/31/2024"
    )

    styled_balance_df = apply_balance_styles(balance_df)

    balance_df["Saldo Inicial"] = balance_df["Saldo Inicial"].apply(
        lambda x: f"R${x:,.2f}"
    )
    balance_df["Valor Previsto de Transações"] = balance_df[
        "Valor Previsto de Transações"
    ].apply(lambda x: f"R${x:,.2f}")
    balance_df["Saldo Previsto"] = balance_df["Saldo Previsto"].apply(
        lambda x: f"R${x:,.2f}"
    )

    st.write(styled_balance_df.to_html(), unsafe_allow_html=True)


def edit_balance():
    st.subheader("Editar Saldo Inicial")

    # Verifique se balance_df está no estado da sessão
    if "balance_df" not in st.session_state or st.session_state.balance_df.empty:
        st.write("Nenhum dado de balanço disponível.")
        return

    # Copie o balance_df para evitar manipulações diretas no estado da sessão
    balance_df = st.session_state.balance_df.copy()

    # Escolha a data para alterar o saldo
    data_to_edit = st.date_input(
        "Escolha a data para alterar o saldo", value=datetime.today()
    )
    novo_saldo = st.number_input(
        "Novo Saldo Inicial (R$)", min_value=0.00, format="%.2f", step=0.01
    )

    if data_to_edit:
        data_to_edit_str = data_to_edit.strftime("%d/%m/%Y")
        if st.button("Atualizar Saldo Inicial"):
            # Verifique se a data escolhida está no DataFrame
            if data_to_edit_str in balance_df["Data"].values:
                saldo_anterior = balance_df.loc[
                    balance_df["Data"] == data_to_edit_str, "Saldo Inicial"
                ].values[0]
                ajuste_valor = novo_saldo - saldo_anterior
                nova_transacao = pd.DataFrame(
                    [
                        {
                            "Tipo": "Receita" if ajuste_valor > 0 else "Gasto",
                            "Categoria": "Ajuste de Saldo",
                            "Classe": "",
                            "Origem": "",
                            "Descrição": "Ajuste de Saldo Inicial",
                            "Valor": abs(ajuste_valor),
                            "Observação": "",
                            "Data": data_to_edit_str,
                            "MesAno": data_to_edit.strftime("%Y/%m"),
                            "Inclusão": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                            "Realizado": True,
                        }
                    ]
                )
                # Adicione a nova transação ao DataFrame de transações
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
                st.session_state.df = pd.concat(
                    [st.session_state.df, nova_transacao], ignore_index=True
                )
                st.success(
                    f"Transação de ajuste de saldo criada: {nova_transacao['Tipo'].values[0]} de R$ {nova_transacao['Valor'].values[0]:.2f}"
                )
                st.rerun()  # Atualiza a página para refletir as mudanças
            else:
                st.error("Data não encontrada no balanço financeiro.")

    st.write("Balanço Financeiro Atualizado:")
    st.dataframe(balance_df)


def show_dashboard():
    return


if __name__ == "__main__":
    view_data()
