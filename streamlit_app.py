import streamlit as st
import src.data_processing as dp
import src.data_visualization as dv
import src.file_handling as fh
import src.manual_entry as me


def main():
    st.title("Aplicação de Finanças Pessoais")
    menu = ["Home", "Upload JSON", "Manual Entry", "Dashboard", "Visualização de Dados"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.write("Bem-vindo à Aplicação de Finanças Pessoais.")

    elif choice == "Upload JSON":
        fh.upload_json()

    elif choice == "Manual Entry":
        me.manual_entry()

    elif choice == "Dashboard":
        dv.show_dashboard()

    elif choice == "Visualização de Dados":
        dv.view_data()


if __name__ == "__main__":
    main()
