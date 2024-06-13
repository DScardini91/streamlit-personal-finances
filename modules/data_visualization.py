import streamlit as st

def view_data():
    st.subheader("Visualização dos dados")

    if not st.session_state.df.empty:
        # Filtros
        tipos = st.multiselect("Tipo", options=st.session_state.df['Tipo'].unique())
        categorias = st.multiselect("Categoria", options=st.session_state.df['Categoria'].unique())
        classes = st.multiselect("Classe", options=st.session_state.df['Classe'].unique())
        subclasses = st.multiselect("Subclasse", options=st.session_state.df['Subclasse'].unique())
        meses = st.multiselect("Mês/Ano", options=st.session_state.df['MesAno'].unique())

        filtered_df = st.session_state.df.copy()

        if tipos:
            filtered_df = filtered_df[filtered_df['Tipo'].isin(tipos)]
        if categorias:
            filtered_df = filtered_df[filtered_df['Categoria'].isin(categorias)]
        if classes:
            filtered_df = filtered_df[filtered_df['Classe'].isin(classes)]
        if subclasses:
            filtered_df = filtered_df[filtered_df['Subclasse'].isin(subclasses)]
        if meses:
            filtered_df = filtered_df[filtered_df['MesAno'].isin(meses)]

        st.write("Transações Filtradas:")
        st.dataframe(filtered_df.drop(columns=['Inclusão']))
    else:
        st.write("Nenhum dado disponível. Carregue os dados para visualizar.")

def show_dashboard():
    return