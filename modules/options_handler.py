import streamlit as st
import json


def load_options():
    # Verifica se já existem opções no session_state
    if "options" in st.session_state:
        return st.session_state.options

    # Tenta carregar opções do options.json
    try:
        with open("modules/options.json", "r") as f:
            options = json.load(f)
    except FileNotFoundError:
        options = {
            "tipo_options": [],
            "categoria_options": {},
            "classe_options": {},
            "subclasse_options": {},
            "origem_options": {},
        }

    # Atualiza o session_state com as opções carregadas
    st.session_state.options = options
    return options


def save_options(options):
    # Atualiza o session_state com as novas opções
    st.session_state.options = options


def add_class_to_category(tipo, category, new_class):
    options = st.session_state.options
    if category in options["categoria_options"].get(tipo, []):
        if new_class not in options["classe_options"].get(category, []):
            options["classe_options"].setdefault(category, []).append(new_class)
            save_options(options)
            return True
    return False


def remove_class_from_category(tipo, category, class_to_remove):
    options = st.session_state.options
    if category in options["categoria_options"].get(tipo, []):
        if class_to_remove in options["classe_options"].get(category, []):
            options["classe_options"][category].remove(class_to_remove)
            save_options(options)
            return True
    return False


def add_subclass_to_class(tipo, category, classe, new_subclass):
    options = st.session_state.options
    if category in options["categoria_options"].get(tipo, []):
        if classe in options["classe_options"].get(category, []):
            if new_subclass not in options["subclasse_options"].get(classe, []):
                options["subclasse_options"].setdefault(classe, []).append(new_subclass)
                save_options(options)
                return True
    return False


def remove_subclass_from_class(tipo, category, classe, subclass_to_remove):
    options = st.session_state.options
    if category in options["categoria_options"].get(tipo, []):
        if classe in options["classe_options"].get(category, []):
            if subclass_to_remove in options["subclasse_options"].get(classe, []):
                options["subclasse_options"][classe].remove(subclass_to_remove)
                save_options(options)
                return True
    return False
