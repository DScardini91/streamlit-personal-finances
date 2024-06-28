import pandas as pd
from datetime import datetime
import os


def load_card_data():
    # Configuração constante dos cartões
    return pd.DataFrame(
        {
            "Cartão": ["Elo", "Mastercard", "Visa"],
            "Dia de Pagamento": [25, 25, 11],
            "Dia de Fechamento": [12, 12, 27],
        }
    )


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

        card_transactions["Pagamento"] = card_transactions["Fechamento"].apply(
            lambda x: (
                (x + pd.DateOffset(months=1)).replace(day=payment_day)
                if card_name == "Visa"
                else (
                    x.replace(day=payment_day)
                    if x.day <= payment_day
                    else (x + pd.DateOffset(months=1)).replace(day=payment_day)
                )
            )
        )

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
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y").dt.date
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
                "Data": statement["Pagamento"].strftime("%d/%m/%Y"),
                "MesAno": statement["Pagamento"].strftime("%Y/%m"),
                "Inclusão": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "Realizado": False,
            }
            for statement in card_statements
        ]
    )

    df = df[
        ~(
            (df["Descrição"].str.startswith("Pagamento de Fatura "))
            & (df["Tipo"] == "Gasto")
            & (df["Origem"] == "Conta Corrente")
        )
    ]

    df = pd.concat([df, statement_transactions], ignore_index=True)

    df["Data"] = pd.to_datetime(
        df["Data"], format="%d/%m/%Y"
    ).dt.date  # Garantir que todas as datas estejam no formato datetime.date
    df["Valor"] = df.apply(
        lambda x: -abs(x["Valor"]) if x["Tipo"] == "Gasto" else abs(x["Valor"]), axis=1
    )

    df_past = df[(df["Data"] <= today) & (df["Realizado"] == True)]
    df_future = df[(df["Data"] > today) & (df["Origem"] == "Conta Corrente")]

    df_filtered = pd.concat([df_past, df_future])

    dates = pd.date_range(start=start_date, end=end_date, freq="D").date
    balance_df = pd.DataFrame(dates, columns=["Data"])

    df_filtered = df_filtered.sort_values(by="Data")

    daily_transactions = (
        df_filtered.groupby("Data")["Valor"]
        .sum()
        .reset_index(name="Valor Previsto de Transações")
    )

    balance_df = balance_df.merge(daily_transactions, on="Data", how="left").fillna(0)

    balance_df["Saldo Inicial"] = 0
    saldo_previsto = 0
    for i in range(len(balance_df)):
        balance_df.at[i, "Saldo Inicial"] = saldo_previsto
        saldo_previsto = (
            balance_df.at[i, "Saldo Inicial"]
            + balance_df.at[i, "Valor Previsto de Transações"]
        )
        balance_df.at[i, "Saldo Previsto"] = saldo_previsto

    balance_df["Data"] = balance_df["Data"].map(lambda x: x.strftime("%d/%m/%Y"))

    return balance_df.reset_index(drop=True), card_statements
