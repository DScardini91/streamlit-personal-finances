import streamlit as st
import pandas as pd


def view_data():
    st.subheader("Visualização de Dados")

    # Upload do arquivo Parquet
    uploaded_file = st.file_uploader("Escolha um arquivo", type=["parquet"])
    if uploaded_file:
        df = pd.read_parquet(uploaded_file)

        # Exibir tabela completa
        st.write("Tabela Completa")
        st.dataframe(df)

        # Filtros
        st.write("Filtros")
        tipo_filter = st.multiselect(
            "Tipo", options=df["Tipo"].unique(), default=df["Tipo"].unique()
        )
        categoria_filter = st.multiselect(
            "Categoria",
            options=df["Categoria"].unique(),
            default=df["Categoria"].unique(),
        )
        classe_filter = st.multiselect(
            "Classe", options=df["Classe"].unique(), default=df["Classe"].unique()
        )

        # Aplicar filtros
        filtered_df = df[
            (df["Tipo"].isin(tipo_filter))
            & (df["Categoria"].isin(categoria_filter))
            & (df["Classe"].isin(classe_filter))
        ]

        st.write("Tabela Filtrada")
        st.dataframe(filtered_df)
