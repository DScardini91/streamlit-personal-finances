import pandas as pd
import streamlit as st
import plotly.express as px
from modules.data_processing import calculate_balance


# Carregar os dados
def load_data():
    if "df" not in st.session_state or st.session_state.df.empty:
        st.error("Nenhum dado de transação disponível.")
        return pd.DataFrame(), pd.DataFrame()
    balance_df, card_statements = calculate_balance(
        st.session_state.df, "01/01/2024", "31/12/2024"
    )
    return st.session_state.df, balance_df


# Função para criar os gráficos
def create_dashboard():
    df, balance_df = load_data()

    if df.empty or balance_df.empty:
        st.write("Nenhum dado de transação disponível.")
        return

    # Certificar que a coluna "Data" está no formato datetime
    df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")

    # Gráfico de Barras: Metas x Gastos Percentuais
    def create_goal_vs_spent_bar_chart():
        category_totals = df[df["Tipo"] == "Gasto"].groupby("Categoria")["Valor"].sum()
        total_spent = category_totals.sum()
        categories = list(st.session_state.goals.keys())
        goal_values = [st.session_state.goals[cat] for cat in categories]
        spent_values = [
            (category_totals.get(cat, 0) / total_spent) * 100 if total_spent != 0 else 0
            for cat in categories
        ]

        data = {
            "Categorias": categories,
            "Metas (%)": goal_values,
            "Gastos (%)": spent_values,
        }
        df_bar = pd.DataFrame(data)

        fig = px.bar(
            df_bar,
            x="Categorias",
            y=["Metas (%)", "Gastos (%)"],
            barmode="group",
            title="Metas vs Gastos Percentuais",
            color_discrete_map={"Metas (%)": "darkblue", "Gastos (%)": "lightblue"},
        )
        return fig

    # Gráfico de Barras Verticais: P&L
    def create_pnl_bar_chart():
        monthly_totals = (
            df.groupby(df["Data"].dt.to_period("M"))["Valor"].sum().reset_index()
        )
        monthly_totals["Data"] = monthly_totals["Data"].dt.to_timestamp()
        colors = ["green" if x > 0 else "red" for x in monthly_totals["Valor"]]
        monthly_totals["Color"] = colors

        fig = px.bar(
            monthly_totals,
            x="Data",
            y="Valor",
            color="Color",
            title="P&L Mensal",
            color_discrete_map={"green": "green", "red": "red"},
        )
        return fig

    # Gráfico de Linhas: Receitas e Gastos
    def create_revenue_expense_line_chart():
        monthly_data = (
            df.groupby([df["Data"].dt.to_period("M"), "Tipo"])["Valor"]
            .sum()
            .unstack()
            .reset_index()
        )
        monthly_data["Data"] = monthly_data["Data"].dt.to_timestamp()

        fig = px.line(
            monthly_data,
            x="Data",
            y=["Receita", "Gasto"],
            title="Receitas e Gastos Mensais",
        )
        fig.update_layout(yaxis_title="Valor")
        return fig

    # Quarta visualização: Gráfico de Pizza das Categorias de Gastos
    def create_expense_pie_chart():
        category_totals = (
            df[df["Tipo"] == "Gasto"].groupby("Categoria")["Valor"].sum().reset_index()
        )
        fig = px.pie(
            category_totals,
            values="Valor",
            names="Categoria",
            title="Distribuição de Gastos por Categoria",
        )
        return fig

    # Renderizar os gráficos usando Plotly
    st.plotly_chart(create_goal_vs_spent_bar_chart(), use_container_width=True)
    st.plotly_chart(create_pnl_bar_chart(), use_container_width=True)
    st.plotly_chart(create_revenue_expense_line_chart(), use_container_width=True)
    st.plotly_chart(create_expense_pie_chart(), use_container_width=True)


# Função principal do Streamlit
def main():
    st.title("Dashboard Financeiro")

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

    # Renderizar o dashboard
    create_dashboard()


if __name__ == "__main__":
    main()
