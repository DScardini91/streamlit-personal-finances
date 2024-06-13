import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Inicializa um DataFrame vazio se não existir
def initialize_df():
    if 'df' not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=[
            'Tipo', 'Categoria', 'Classe', 'Subclasse', 'Descrição', 'Valor', 'Observação', 'Data', 'MesAno', 'Inclusão'
        ])

def save_data(file_name):
    file_name = f"{file_name}.parquet" if not file_name.endswith(".parquet") else file_name
    st.session_state.df.to_parquet(file_name)
    st.success(f"Dados salvos em {file_name}")

def load_data(uploaded_file):
    st.session_state.df = pd.read_parquet(uploaded_file)
    st.success("Dados carregados com sucesso")

def manual_entry():
    st.subheader("Adicionar transação comum")

    initialize_df()

    # Define options for dropdown lists with capitalized names
    tipos = ["Gasto", "Previsão de Gasto", "Receita", "Previsão de Receita"]
    categorias = [
        "Custo Fixo",
        "Conforto",
        "Prazeres",
        "Metas",
        "Educação",
        "Investimento",
    ]
    classes = ["Moradia", "Curso", "Saúde", "Alimentação"]
    subclasses = {
        "Moradia": ["Aluguel", "Conta de Luz", "Conta de Água", "Condomínio"],
        "Curso": ["Matrícula", "Material"],
        "Saúde": ["Consulta", "Exame", "Medicamento"],
        "Alimentação": ["Supermercado", "Restaurante"],
    }

    # Inicializa os inputs se não existir
    if 'inputs' not in st.session_state:
        st.session_state.inputs = {
            'tipo': tipos[0],
            'categoria': categorias[0],
            'classe': classes[0],
            'subclasse': '',
            'descricao': '',
            'valor': 0.00,
            'observacao': '',
            'data_transacao': datetime.today()
        }

    col1, col2 = st.columns(2)

    with col1:
        with st.form(key="manual_entry_form"):
            st.session_state.inputs['tipo'] = st.selectbox("Tipo", tipos, index=tipos.index(st.session_state.inputs['tipo']))
            st.session_state.inputs['categoria'] = st.selectbox("Categoria", categorias, index=categorias.index(st.session_state.inputs['categoria']))
            st.session_state.inputs['classe'] = st.selectbox("Classe", classes, index=classes.index(st.session_state.inputs['classe']))
            st.session_state.inputs['subclasse'] = st.selectbox("Subclasse", subclasses.get(st.session_state.inputs['classe'], []), index=0)
            st.session_state.inputs['descricao'] = st.text_input("Descrição", st.session_state.inputs['descricao'])
            st.session_state.inputs['valor'] = st.number_input("Valor (R$)", min_value=0.00, format="%.2f", value=st.session_state.inputs['valor'])
            st.session_state.inputs['observacao'] = st.text_input("Observação", st.session_state.inputs['observacao'])
            st.session_state.inputs['data_transacao'] = st.date_input("Data da Transação", value=st.session_state.inputs['data_transacao'])

            confirm_button = st.form_submit_button(label="✅ Confirmar")
            correct_button = st.form_submit_button(label="🧽 Corrigir")

    if confirm_button:
        # Adiciona a nova transação ao DataFrame
        data_hora_inclusao = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        mes_ano = st.session_state.inputs['data_transacao'].strftime('%m/%Y')
        new_transaction = pd.DataFrame({
            'Tipo': [st.session_state.inputs['tipo']],
            'Categoria': [st.session_state.inputs['categoria']],
            'Classe': [st.session_state.inputs['classe']],
            'Subclasse': [st.session_state.inputs['subclasse']],
            'Descrição': [st.session_state.inputs['descricao']],
            'Valor': [st.session_state.inputs['valor']],
            'Observação': [st.session_state.inputs['observacao']],
            'Data': [st.session_state.inputs['data_transacao'].strftime('%d/%m/%Y')],
            'MesAno': [mes_ano],
            'Inclusão': [data_hora_inclusao]
        })
        st.session_state.df = pd.concat([st.session_state.df, new_transaction], ignore_index=True)
        
        st.success(f"Adicionado: {st.session_state.inputs['descricao']} de valor R${st.session_state.inputs['valor']:.2f} como {st.session_state.inputs['tipo']} em {st.session_state.inputs['data_transacao'].strftime('%d/%m/%Y')}")

    if correct_button:
        st.session_state.inputs = {
            'tipo': tipos[0],
            'categoria': categorias[0],
            'classe': classes[0],
            'subclasse': '',
            'descricao': '',
            'valor': 0.00,
            'observacao': '',
            'data_transacao': datetime.today()
        }
        st.warning("Corrigir entrada. Por favor, preencha novamente os campos.")

    with col2:
        # Exibir o DataFrame atualizado, ordenado por data e hora de inclusão
        st.write("Transações Registradas:")
        if not st.session_state.df.empty:
            st.session_state.df = st.session_state.df.sort_values(by='Inclusão', ascending=False)
            # Remove a coluna 'Inclusão' antes de exibir o DataFrame
            st.dataframe(st.session_state.df.drop(columns=['Inclusão']).reset_index(drop=True))

def recurring_entry():
    st.subheader("Adicionar transação recorrente")

    initialize_df()

    # Define options for dropdown lists with capitalized names
    tipos = ["Gasto", "Previsão de Gasto", "Receita", "Previsão de Receita"]
    categorias = [
        "Custo Fixo",
        "Conforto",
        "Prazeres",
        "Metas",
        "Educação",
        "Investimento",
    ]
    classes = ["Moradia", "Curso", "Saúde", "Alimentação"]
    subclasses = {
        "Moradia": ["Aluguel", "Conta de Luz", "Conta de Água", "Condomínio"],
        "Curso": ["Matrícula", "Material"],
        "Saúde": ["Consulta", "Exame", "Medicamento"],
        "Alimentação": ["Supermercado", "Restaurante"],
    }

    # Inicializa os inputs se não existir
    if 'recurring_inputs' not in st.session_state:
        st.session_state.recurring_inputs = {
            'tipo': tipos[0],
            'categoria': categorias[0],
            'classe': classes[0],
            'subclasse': '',
            'descricao': '',
            'valor': 0.00,
            'observacao': '',
            'data_inicio': datetime.today(),
            'periodicidade': 1,
            'duracao': 1
        }

    col1, col2 = st.columns(2)

    with col1:
        with st.form(key="recurring_entry_form"):
            st.session_state.recurring_inputs['tipo'] = st.selectbox("Tipo", tipos, index=tipos.index(st.session_state.recurring_inputs['tipo']))
            st.session_state.recurring_inputs['categoria'] = st.selectbox("Categoria", categorias, index=categorias.index(st.session_state.recurring_inputs['categoria']))
            st.session_state.recurring_inputs['classe'] = st.selectbox("Classe", classes, index=classes.index(st.session_state.recurring_inputs['classe']))
            st.session_state.recurring_inputs['subclasse'] = st.selectbox("Subclasse", subclasses.get(st.session_state.recurring_inputs['classe'], []), index=0)
            st.session_state.recurring_inputs['descricao'] = st.text_input("Descrição", st.session_state.recurring_inputs['descricao'])
            st.session_state.recurring_inputs['valor'] = st.number_input("Valor (R$)", min_value=0.00, format="%.2f", value=st.session_state.recurring_inputs['valor'])
            st.session_state.recurring_inputs['observacao'] = st.text_input("Observação", st.session_state.recurring_inputs['observacao'])
            st.session_state.recurring_inputs['data_inicio'] = st.date_input("Data de Início", value=st.session_state.recurring_inputs['data_inicio'])
            st.session_state.recurring_inputs['periodicidade'] = st.number_input("Periodicidade (em meses)", min_value=1, step=1, value=st.session_state.recurring_inputs['periodicidade'])
            st.session_state.recurring_inputs['duracao'] = st.number_input("Duração (em meses)", min_value=1, step=1, value=st.session_state.recurring_inputs['duracao'])

            confirm_button = st.form_submit_button(label="✅ Confirmar")
            correct_button = st.form_submit_button(label="🧽 Corrigir")

    if confirm_button:
        data_hora_inclusao = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        for i in range(0, st.session_state.recurring_inputs['duracao'], st.session_state.recurring_inputs['periodicidade']):
            data_transacao = st.session_state.recurring_inputs['data_inicio'] + relativedelta(months=i)
            mes_ano = data_transacao.strftime('%m/%Y')
            new_transaction = pd.DataFrame({
                'Tipo': [st.session_state.recurring_inputs['tipo']],
                'Categoria': [st.session_state.recurring_inputs['categoria']],
                'Classe': [st.session_state.recurring_inputs['classe']],
                'Subclasse': [st.session_state.recurring_inputs['subclasse']],
                'Descrição': [st.session_state.recurring_inputs['descricao']],
                'Valor': [st.session_state.recurring_inputs['valor']],
                'Observação': [st.session_state.recurring_inputs['observacao']],
                'Data': [data_transacao.strftime('%d/%m/%Y')],
                'MesAno': [mes_ano],
                'Inclusão': [data_hora_inclusao]
            })
            st.session_state.df = pd.concat([st.session_state.df, new_transaction], ignore_index=True)
        
        st.success(f"Transação recorrente adicionada: {st.session_state.recurring_inputs['descricao']} de valor R${st.session_state.recurring_inputs['valor']:.2f} como {st.session_state.recurring_inputs['tipo']} iniciando em {st.session_state.recurring_inputs['data_inicio'].strftime('%d/%m/%Y')}")

    if correct_button:
        st.session_state.recurring_inputs = {
            'tipo': tipos[0],
            'categoria': categorias[0],
            'classe': classes[0],
            'subclasse': '',
            'descricao': '',
            'valor': 0.00,
            'observacao': '',
            'data_inicio': datetime.today(),
            'periodicidade': 1,
            'duracao': 1
        }
        st.warning("Corrigir entrada. Por favor, preencha novamente os campos.")

    with col2:
        # Exibir o DataFrame atualizado, ordenado por data e hora de inclusão
        st.write("Transações Registradas:")
        if not st.session_state.df.empty:
            st.session_state.df = st.session_state.df.sort_values(by='Inclusão', ascending=False)
            # Remove a coluna 'Inclusão' antes de exibir o DataFrame
            st.dataframe(st.session_state.df.drop(columns=['Inclusão']).reset_index(drop=True))

if __name__ == "__main__":
    manual_entry()
