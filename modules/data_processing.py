import pandas as pd
from datetime import datetime
import os


def load_card_data():
    if os.path.exists("cards.parquet"):
        return pd.read_parquet("cards.parquet")
    else:
        return pd.DataFrame(columns=["Cartão", "Dia de Pagamento", "Dia de Fechamento"])


def calculate_card_statements(df, card_data):
    statements = []

    for _, card in card_data.iterrows():
        card_name = card["Cartão"]
        payment_day = card["Dia de Pagamento"]
        closing_day = card["Dia de Fechamento"]

        card_transactions = df[(df["Origem"] == card_name) & (df["Tipo"] == "Gasto")]

        if card_transactions.empty:
            continue

        card_transactions = card_transactions.sort_values(by="Data")

        card_transactions["Fechamento"] = card_transactions["Data"].apply(
            lambda x: (
                x.replace(day=closing_day)
                if x.day <= closing_day
                else (x + pd.DateOffset(months=1)).replace(day=closing_day)
            )
        )

        card_transactions["Pagamento"] = card_transactions[
            "Fechamento"
        ] + pd.DateOffset(days=(payment_day - closing_day))

        grouped = card_transactions.groupby(["Fechamento", "Pagamento"])

        for (fechamento, pagamento), group in grouped:
            statement_total = group["Valor"].sum()
            if statement_total > 0:
                statement = {
                    "Cartão": card_name,
                    "Fechamento": fechamento,
                    "Pagamento": pagamento,
                    "Total": statement_total,
                    "Transações": group,
                }
                statements.append(statement)

    return statements


def calculate_balance(df, start_date, end_date):
    df["Data"] = pd.to_datetime(df["Data"]).dt.date
    today = datetime.today().date()
    card_data = load_card_data()

    card_statements = calculate_card_statements(df, card_data)

    statement_transactions = pd.DataFrame(
        [
            {
                "Tipo": "Gasto",
                "Categoria": "Pagamento de Fatura",
                "Classe": "",
                "Origem": "Conta Corrente",
                "Descrição": f'Pagamento de Fatura {statement["Cartão"]}',
                "Valor": statement["Total"],
                "Observação": "",
                "Data": statement["Pagamento"].date(),
                "MesAno": statement["Pagamento"].strftime("%Y/%m"),
                "Inclusão": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Realizado": False,
            }
            for statement in card_statements
        ]
    )

    # Remover transações antigas de pagamento de faturas
    df = df[
        ~(
            (df["Descrição"].str.startswith("Pagamento de Fatura "))
            & (df["Tipo"] == "Gasto")
            & (df["Origem"] == "Conta Corrente")
        )
    ]

    # Adicionar as novas transações de pagamento de faturas
    df = pd.concat([df, statement_transactions], ignore_index=True)

    # Manter gastos negativos e receitas positivas
    df["Valor"] = df.apply(
        lambda x: -abs(x["Valor"]) if x["Tipo"] == "Gasto" else abs(x["Valor"]), axis=1
    )

    # Filtrar as transações para incluir apenas as realizadas em datas passadas e futuras
    df_past = df[(df["Data"] <= today) & (df["Realizado"] == True)]
    df_future = df[(df["Data"] > today) & (df["Origem"] == "Conta Corrente")]

    # Concatenar os dataframes filtrados
    df_filtered = pd.concat([df_past, df_future])

    # Gerar um DataFrame com todas as datas no intervalo
    dates = pd.date_range(start=start_date, end=end_date, freq="D").date
    balance_df = pd.DataFrame(dates, columns=["Data"])

    # Ordenar o DataFrame pela data
    df_filtered = df_filtered.sort_values(by="Data")

    # Agrupar por data e calcular o valor total das transações de cada dia
    daily_transactions = (
        df_filtered.groupby("Data")["Valor"]
        .sum()
        .reset_index(name="Valor Previsto de Transações")
    )

    saldo_inicial = 0
    balance_df["Saldo Inicial"] = saldo_inicial
    balance_df["Valor Previsto de Transações"] = 0.00
    balance_df["Saldo Previsto"] = saldo_inicial

    balance_df.set_index("Data", inplace=True)
    balance_df.update(daily_transactions.set_index("Data"))
    balance_df = balance_df.fillna(0)

    balance_df["Saldo Previsto"] = (
        saldo_inicial + balance_df["Valor Previsto de Transações"].cumsum()
    )
    balance_df["Data"] = balance_df.index.map(lambda x: x.strftime("%d/%m/%Y"))

    return balance_df.reset_index(drop=True), card_statements


if __name__ == "__main__":
    calculate_balance()
