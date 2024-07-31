import streamlit as st
from modules.options_handler import load_options, save_options
import pandas as pd


def show_classes(options, selected_categorias, selected_classes, selected_subclasses):
    st.write("### Hierarquia de Categorias, Classes e Subclasses")

    data = []
    for tipo, categorias in options["categoria_options"].items():
        for categoria in categorias:
            if selected_categorias and categoria not in selected_categorias:
                continue
            classes = options["classe_options"].get(categoria, [])
            for classe in classes:
                if selected_classes and classe not in selected_classes:
                    continue
                subclasses = options["subclasse_options"].get(classe, [])
                if subclasses:
                    for subclass in subclasses:
                        if selected_subclasses and subclass not in selected_subclasses:
                            continue
                        data.append([tipo, categoria, classe, subclass])
                else:
                    data.append([tipo, categoria, classe, ""])

    df = pd.DataFrame(data, columns=["Tipo", "Categoria", "Classe", "Subclasse"])
    st.dataframe(
        df[["Tipo", "Categoria", "Classe", "Subclasse"]],
        use_container_width=True,
        hide_index=True,
        height=600,
    )


def add_class_to_category(tipo, category, new_class):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if new_class not in options["classe_options"].get(category, []):
            options["classe_options"].setdefault(category, []).append(new_class)
            save_options(options)
            st.session_state.options = options  # Atualiza o session_state
            return True
    return False


def remove_class_from_category(tipo, category, class_to_remove):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if class_to_remove in options["classe_options"].get(category, []):
            options["classe_options"][category].remove(class_to_remove)
            save_options(options)
            st.session_state.options = options  # Atualiza o session_state
            return True
    return False


def add_subclass_to_class(tipo, category, classe, new_subclass):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if classe in options["classe_options"].get(category, []):
            if new_subclass not in options["subclasse_options"].get(classe, []):
                options["subclasse_options"].setdefault(classe, []).append(new_subclass)
                save_options(options)
                st.session_state.options = options  # Atualiza o session_state
                return True
    return False


def remove_subclass_from_class(tipo, category, classe, subclass_to_remove):
    options = load_options()
    if category in options["categoria_options"].get(tipo, []):
        if classe in options["classe_options"].get(category, []):
            if subclass_to_remove in options["subclasse_options"].get(classe, []):
                options["subclasse_options"][classe].remove(subclass_to_remove)
                save_options(options)
                st.session_state.options = options  # Atualiza o session_state
                return True
    return False


def manage_hierarchy():
    st.subheader("Gerenciar Hierarquia de Categorias, Classes e Subclasses")

    col1, col2 = st.columns([1, 2])  # Coluna 1 com 33% e Coluna 2 com 67% do espaço

    with col1:
        options = load_options()
        tipo_selecionado = st.selectbox("Selecione o Tipo", options["tipo_options"])
        categoria_selecionada = st.selectbox(
            "Selecione a Categoria",
            options["categoria_options"].get(tipo_selecionado, []),
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

        if acao in ["Adicionar Subclasse", "Remover Subclasse"]:
            classe_selecionada = st.selectbox(
                "Selecione a Classe",
                options["classe_options"].get(categoria_selecionada, []),
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

                st.rerun()

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

        categorias_multiselect = st.multiselect(
            "Filtrar por Categoria",
            options=options["categoria_options"].get(tipo_selecionado, []),
        )
        classes_multiselect = st.multiselect(
            "Filtrar por Classe", options=sum(options["classe_options"].values(), [])
        )
        subclasses_multiselect = st.multiselect(
            "Filtrar por Subclasse",
            options=sum(options["subclasse_options"].values(), []),
        )

    with col2:

        show_classes(
            options, categorias_multiselect, classes_multiselect, subclasses_multiselect
        )

    # Atualiza o session_state com as opções modificadas
    st.session_state.options = options


if __name__ == "__main__":
    manage_hierarchy()
