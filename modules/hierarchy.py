import streamlit as st
import json


def load_options():
    if "options" in st.session_state:
        return st.session_state.options
    with open("modules/options.json", "r") as f:
        options = json.load(f)
    st.session_state.options = options
    return options


def save_options(options):
    with open("modules/options.json", "w") as f:
        json.dump(options, f, indent=4)
    st.session_state.options = options


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


def add_subclass_to_class(tipo, category, classe, new_subclass):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if classe in options["classe_options"].get(category, []):
            if new_subclass not in options["subclasse_options"].get(classe, []):
                options["subclasse_options"].setdefault(classe, []).append(new_subclass)
                save_options(options)
                return True
    return False


def remove_subclass_from_class(tipo, category, classe, subclass_to_remove):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if classe in options["classe_options"].get(category, []):
            if subclass_to_remove in options["subclasse_options"].get(classe, []):
                options["subclasse_options"][classe].remove(subclass_to_remove)
                save_options(options)
                return True
    return False


def show_classes(options):
    st.write("### Hierarquia de Categorias, Classes e Subclasses")
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
                subclasses = options["subclasse_options"].get(classe, [])
                for subclass in subclasses:
                    st.markdown(
                        f"<p class='small-font' style='margin-left: 20px;'>-- {subclass}</p>",
                        unsafe_allow_html=True,
                    )


def manage_hierarchy():
    st.subheader("Gerenciar Hierarquia de Categorias, Classes e Subclasses")

    col1, col2 = st.columns(2)

    with col1:
        options = load_options()
        tipo_selecionado = st.selectbox("Selecione o Tipo", options["tipo_options"])
        categoria_selecionada = st.selectbox(
            "Selecione a Categoria",
            options["categoria_options"].get(tipo_selecionado, []),
        )
        classe_selecionada = st.selectbox(
            "Selecione a Classe",
            options["classe_options"].get(categoria_selecionada, []),
        )

        acao = st.radio(
            "Ação",
            (
                "Adicionar Classe",
                "Remover Classe",
                "Adicionar Subclasse",
                "Remover Subclasse",
            ),
        )

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

                st.experimental_rerun()

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

        elif acao == "Adicionar Subclasse":
            nova_subclasse = st.text_input("Digite a nova Subclasse")

            if st.button("Adicionar Subclasse"):
                if add_subclass_to_class(
                    tipo_selecionado,
                    categoria_selecionada,
                    classe_selecionada,
                    nova_subclasse,
                ):
                    st.success(
                        f"Subclasse '{nova_subclasse}' adicionada à classe '{classe_selecionada}' com sucesso."
                    )
                else:
                    st.error(
                        "Erro ao adicionar a subclasse. Verifique se a classe existe e tente novamente."
                    )

                st.experimental_rerun()

        elif acao == "Remover Subclasse":
            subclasses_existentes = options["subclasse_options"].get(
                classe_selecionada, []
            )
            subclasse_selecionada = st.selectbox(
                "Selecione a Subclasse para remover", subclasses_existentes
            )

            if st.button("Remover Subclasse"):
                if remove_subclass_from_class(
                    tipo_selecionado,
                    categoria_selecionada,
                    classe_selecionada,
                    subclasse_selecionada,
                ):
                    st.success(
                        f"Subclasse '{subclasse_selecionada}' removida da classe '{classe_selecionada}' com sucesso."
                    )
                else:
                    st.error(
                        "Erro ao remover a subclasse. Verifique se a subclasse existe e tente novamente."
                    )

    with col2:
        show_classes(options)


if __name__ == "__main__":
    manage_hierarchy()
