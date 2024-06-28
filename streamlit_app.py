import streamlit as st
from modules import data_processing as dp
from modules import data_visualization as dv
from modules import file_handling as fh
from modules import manual_entry as me
from modules import cards as cd
from modules import hierarchy as hy
from modules import home as hm  # Importar o novo módulo home

# Configuração do tema personalizado para Streamlit
st.set_page_config(
    page_title="Aplicação de Finanças Pessoais",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Adicione este trecho de CSS no início do arquivo streamlit_app.py para um tema escuro e acessível
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .css-1aumxhk, .css-145kmo2 {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
    }
    .stButton>button {
        background-color: #238636 !important;
        color: #FFFFFF !important;
        font-size: 14px !important;
    }
    .stDateInput>div>div {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        font-size: 14px !important;
    }
    .stNumberInput>div>div input {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        font-size: 14px !important;
    }
    .stTextInput>div>div input {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        font-size: 14px !important;
    }
    .stSelectbox>div>div input {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
        font-size: 14px !important;
    }
    .stMarkdown, .stDataFrame, .stCheckbox, .stRadio, .stTextArea {
        color: #c9d1d9 !important;
    }
    .stTable>table>tbody>tr>td, .stTable>table>thead>tr>th {
        background-color: #161b22 !important;
        color: #c9d1d9 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def main():
    st.title("Aplicação de Finanças Pessoais")

    # Botões para salvar e carregar dados
    with st.sidebar:
        fh.save_data_as()
        fh.download_data()

        uploaded_file = st.file_uploader("Carregar Dados", type=["json"])
        if uploaded_file is not None:
            fh.load_data(uploaded_file)
            st.success("Dados carregados com sucesso")

    # Use tabs for navigation
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
        [
            "Home",
            "Adicionar transação",
            "Dashboard",
            "Visualização dos dados",
            "Balanço Financeiro",
            "Editar Saldo Inicial",
            "Cadastro de Cartões",
            "Gerenciar Hierarquia",
        ]
    )

    with tab1:
        hm.home()

    with tab2:
        me.manual_entry()

    with tab3:
        dv.show_dashboard()

    with tab4:
        dv.view_data()

    with tab5:
        dv.view_balance()

    with tab6:
        dv.edit_balance()

    with tab7:
        cd.card_statements_view()

    with tab8:
        hy.manage_hierarchy()


if __name__ == "__main__":
    main()
