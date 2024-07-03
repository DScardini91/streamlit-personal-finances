import streamlit as st
import plotly.express as px
import pandas as pd

# Valores iniciais sugeridos para cada categoria
initial_goals = {
    "Custos fixos": 55,
    "Prazeres": 10,
    "Conforto": 10,
    "Conhecimento": 5,
    "Liberdade Financeira": 10,
    "Dízimo": 10,
    "Reembolsável": 0,
}


def display_goals():
    st.subheader("Definir Metas para Cada Categoria de Gastos")

    # Inicializa metas se não existirem no session_state
    if "goals" not in st.session_state:
        st.session_state.goals = initial_goals

    col1, col2 = st.columns([1, 2])  # Coluna 1: 33%, Coluna 2: 66%

    with col1:
        for category in initial_goals:
            st.session_state.goals[category] = st.slider(
                label=category,
                min_value=0,
                max_value=100,
                value=st.session_state.goals.get(category, initial_goals[category]),
                key=f"slider_{category}",
            )

    with col2:
        # Criação do gráfico de barras horizontais normalizadas
        goals_df = pd.DataFrame(
            list(st.session_state.goals.items()), columns=["Categoria", "Percentual"]
        )
        fig = px.bar(
            goals_df,
            x="Percentual",
            y="Categoria",
            orientation="h",
            text="Percentual",
            title="Metas de Gastos",
        )
        fig.update_layout(
            xaxis_title="Percentual (%)",
            yaxis_title="Categoria",
            yaxis=dict(categoryorder="total ascending"),
        )

        total_percent = sum(st.session_state.goals.values())
        if total_percent != 100:
            st.warning(
                f"O somatório das metas é {total_percent}%. Ajuste para 100%. Diferença: {100 - total_percent} pontos."
            )

        st.plotly_chart(fig)

    if st.button("Salvar Metas"):
        from modules import file_handling

        file_handling.save_data("metas.json")
        st.success("Metas salvas com sucesso!")


if __name__ == "__main__":
    display_goals()
