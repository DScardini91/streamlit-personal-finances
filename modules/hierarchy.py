import streamlit as st
import json


# Função para carregar opções do arquivo JSON
def load_options():
    with open("modules/options.json", "r") as f:
        options = json.load(f)
    return options


# Função para salvar opções no arquivo JSON
def save_options(options):
    with open("modules/options.json", "w") as f:
        json.dump(options, f, indent=4)


def add_class_to_category(tipo, category, new_class):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if new_class not in options["classe_options"].get(category, []):
            options["classe_options"].setdefault(category, []).append(new_class)
            save_options(options)
            return True
    return False


def remove_class_from_category(tipo, category, class_to_remove):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if class_to_remove in options["classe_options"].get(category, []):
            options["classe_options"][category].remove(class_to_remove)
            save_options(options)
            return True
    return False


def show_classes(options):
    st.write("### Hierarquia de Categorias e Classes")
    st.markdown(
        """
        <style>
        .small-font {
            font-size: 10px;
            line-height: 0.4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    for tipo, categorias in options["categoria_options"].items():
        st.markdown(f"**{tipo}**", unsafe_allow_html=True)
        for categoria in categorias:
            st.markdown(f"**{categoria}**", unsafe_allow_html=True)
            classes = options["classe_options"].get(categoria, [])
            for classe in classes:
                st.markdown(
                    f"<p class='small-font'>- {classe}</p>", unsafe_allow_html=True
                )


def manage_hierarchy():
    st.subheader("Gerenciar Hierarquia de Categorias e Classes")

    col1, col2 = st.columns(2)

    with col1:
        options = load_options()
        tipo_selecionado = st.selectbox("Selecione o Tipo", options["tipo_options"])
        categoria_selecionada = st.selectbox(
            "Selecione a Categoria",
            options["categoria_options"].get(tipo_selecionado, []),
        )

        acao = st.radio("Ação", ("Adicionar Classe", "Remover Classe"))

        if acao == "Adicionar Classe":
            nova_classe = st.text_input("Digite a nova Classe")

            if st.button("Adicionar Classe"):
                if add_class_to_category(
                    tipo_selecionado, categoria_selecionada, nova_classe
                ):
                    st.success(
                        f"Classe '{nova_classe}' adicionada à categoria '{categoria_selecionada}' com sucesso."
                    )
                else:
                    st.error(
                        "Erro ao adicionar a classe. Verifique se a categoria existe e tente novamente."
                    )

                st.rerun()

        elif acao == "Remover Classe":
            classes_existentes = options["classe_options"].get(
                categoria_selecionada, []
            )
            classe_selecionada = st.selectbox(
                "Selecione a Classe para remover", classes_existentes
            )

            if st.button("Remover Classe"):
                if remove_class_from_category(
                    tipo_selecionado, categoria_selecionada, classe_selecionada
                ):
                    st.success(
                        f"Classe '{classe_selecionada}' removida da categoria '{categoria_selecionada}' com sucesso."
                    )
                else:
                    st.error(
                        "Erro ao remover a classe. Verifique se a classe e a categoria existem e tente novamente."
                    )

    with col2:
        show_classes(options)


if __name__ == "__main__":
    manage_hierarchy()
