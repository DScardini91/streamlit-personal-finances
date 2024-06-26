import streamlit as st
from datetime import datetime
from modules.data_processing import calculate_balance
import streamlit_shadcn_ui as ui


def home():
    st.write(
        """
        # Bem-vindo ao seu controle financeiro!

        Aqui você pode adicionar suas transações manualmente ou importar um arquivo para análise.

        Para começar, clique em uma das opções no menu à esquerda.
        """
    )
    return


if __name__ == "__main__":
    home()
