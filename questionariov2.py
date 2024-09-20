import streamlit as st
import pandas as pd

# Título do aplicativo
st.title("Bora passar na prova , Lateral!! :smile:")

# Instruções
st.write("Por favor, escolha uma disciplina e o número do questionário no menu lateral.")

# Função para carregar o arquivo CSV com as perguntas
def carregar_perguntas(arquivo_csv):
    try:
        df = pd.read_csv(arquivo_csv, encoding='utf-8', sep=';')
        df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
        return df
    except FileNotFoundError:
        st.error(f"Arquivo '{arquivo_csv}' não encontrado. Verifique o nome do arquivo.")
        st.stop()  # Para o código aqui caso o arquivo não exista
    except pd.errors.EmptyDataError:
        st.error("O arquivo está vazio. Por favor, adicione perguntas.")
        st.stop()  # Para o código se o arquivo estiver vazio
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()  # Para o código em caso de outro erro

# Menu lateral para seleção de disciplina
st.sidebar.title("Selecione as opções")

# Lista de disciplinas disponíveis
disciplinas = {
    "CAO": "CAO",
    "História": "historia",
    "Geografia": "geografia"
}

# Seleção da disciplina no menu lateral
disciplina_escolhida = st.sidebar.selectbox("Escolha a disciplina:", list(disciplinas.keys()))

# Texto explicativo para o usuário escolher o número do questionário
st.sidebar.write("Escolha o número do questionário:")

# Variável para armazenar o número do questionário selecionado
numero_questionario = None

# Botões para seleção do número do questionário (exemplo com os números 1 a 5)
for i in range(1, 6):  # Você pode ajustar esse intervalo conforme necessário
    if st.sidebar.button(f"{i}"):
        numero_questionario = i

# Verifica se o número do questionário foi selecionado
if numero_questionario is not None:
    # Gerar o nome do arquivo CSV com base na disciplina e no número do questionário
    nome_arquivo = f"perguntas_{disciplinas[disciplina_escolhida]}_{numero_questionario}.csv"

    # Carregar as perguntas do arquivo CSV correspondente
    perguntas_df = carregar_perguntas(nome_arquivo)

    if perguntas_df is not None:
        #st.write(f"Carregando o questionário de **{disciplina_escolhida}**, número **{numero_questionario}**...")

        # Dicionário para armazenar as respostas do usuário
        respostas_usuario = {}

        # Usando expander para colapsar perguntas, caso o questionário seja longo
        #with st.expander("Clique para ver as perguntas"):
            # Loop para gerar as perguntas e alternativas a partir do DataFrame
        for index, row in perguntas_df.iterrows():
            pergunta = row['pergunta']
            alternativas = [row['alternativa1'], row['alternativa2'], row['alternativa3'], row['alternativa4']]
            respostas_usuario[pergunta] = st.radio(pergunta, alternativas)

        # Botão para enviar respostas
        if st.button('Enviar'):
            # Variável para contar acertos
            acertos = 0
            
            # Verificando as respostas
            for index, row in perguntas_df.iterrows():
                pergunta = row['pergunta']
                correta = row['correta']
                if respostas_usuario[pergunta] == correta:
                    acertos += 1
            
            # Exibindo o resultado total
            st.success(f"Você acertou {acertos} de {len(perguntas_df)} perguntas.")
            
            # Mostrando feedback individual para cada pergunta
            for index, row in perguntas_df.iterrows():
                pergunta = row['pergunta']
                correta = row['correta']
                if respostas_usuario[pergunta] == correta:
                    st.write(f"{pergunta} - Correto! ✅")
                else:
                    st.write(f"{pergunta} - Incorreto ❌")
else:
    st.sidebar.warning("Por favor, selecione o número do questionário para continuar.")
