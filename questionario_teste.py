import os
import streamlit as st
import pandas as pd

# Título do aplicativo
st.title("Bora passar na prova , Lateral!! 😄")

# Instruções
st.write("Por favor, escolha uma disciplina e o número do questionário no menu lateral.")

# Dicionário com os textos personalizados para cada disciplina
subtitulos_disciplinas = {
    "CAO": "Características Organizacionais",
    "GP": "Gestão de Projetos",
    "GPC": "Gestão Patrimonial",
    "LE": "Liderança e Equipes",
    "PAI": "Processos Avaliativos e Inovação"
}

# Função para carregar o arquivo CSV com as perguntas
def carregar_perguntas(arquivo_csv):
    try:
        df = pd.read_csv(arquivo_csv, encoding='utf-8', sep=';')
        df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
        return df
    except FileNotFoundError:
        st.error(f"Arquivo '{arquivo_csv}' não encontrado. Verifique o nome do arquivo.")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("O arquivo está vazio. Por favor, adicione perguntas.")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()

# Função para identificar os números de questionários disponíveis
def obter_numeros_questionarios(disciplina_abreviacao):
    caminho_arquivos = "C:/Users/COMARA/Documents/RAFAEL/PYTHON/STREAMLIT"
    arquivos = os.listdir(caminho_arquivos)
    numeros = [
        int(nome.split('_')[-1].split('.')[0])
        for nome in arquivos
        if nome.startswith(f"perguntas_{disciplina_abreviacao}_") and nome.endswith(".csv")
    ]
    return sorted(numeros)

# Menu lateral para seleção de disciplina
st.sidebar.title("Selecione as opções :arrow_down:")

# Lista de disciplinas disponíveis
disciplinas = {
    "CAO - Características Organizacionais": "CAO",
    "GP - Gestão de Projetos": "GP",
    "GPC - Gestão Patrimonial": "GPC",
    "LE - Liderança e Equipes": "LE",
    "PAI - Processos Avaliativos e Inovação": "PAI"
}

# Seleção da disciplina no menu lateral
disciplina_escolhida = st.sidebar.selectbox("Escolha a disciplina:", ["Selecione..."] + list(disciplinas.keys()))

# Somente mostra a seleção do número do questionário se uma disciplina for escolhida
if disciplina_escolhida != "Selecione...":
    abreviacao = disciplinas[disciplina_escolhida]
    questionarios_disponiveis = obter_numeros_questionarios(abreviacao)
    numero_questionario = st.sidebar.selectbox("Escolha o número do questionário:", ["Selecione..."] + questionarios_disponiveis)
else:
    numero_questionario = None

# Verifica se a disciplina e o número do questionário foram escolhidos
if disciplina_escolhida != "Selecione..." and numero_questionario != "Selecione...":
    # Exibe o subtítulo com a disciplina escolhida e o número do questionário
    subtitulo = subtitulos_disciplinas.get(abreviacao, disciplina_escolhida)
    st.subheader(f"Disciplina: {subtitulo} | Questionário: {numero_questionario}")

    # Gerar o nome do arquivo CSV com base na disciplina e no número do questionário
    nome_arquivo = f"C:/Users/COMARA/Documents/RAFAEL/PYTHON/STREAMLIT/perguntas_{abreviacao}_{numero_questionario}.csv"

    # Carregar as perguntas do arquivo CSV correspondente
    perguntas_df = carregar_perguntas(nome_arquivo)

    if perguntas_df is not None:
        # Se o número do questionário mudar, resetar as respostas e acertos
        if f'respostas_{numero_questionario}' not in st.session_state:
            st.session_state[f'respostas_{numero_questionario}'] = {}
            st.session_state.acertos = 0

        respostas_usuario = st.session_state[f'respostas_{numero_questionario}']

        # Loop para gerar as perguntas e alternativas a partir do DataFrame
        for index, row in perguntas_df.iterrows():
            pergunta = row['pergunta']
            alternativas = [row['alternativa1'], row['alternativa2'], row['alternativa3'], row['alternativa4']]

            # Pergunta com número da questão, em negrito, e com fonte maior
            st.markdown(
                f"<strong style='font-size: 18px; margin-bottom: 5px;'>Questão {index + 1}: {pergunta}</strong>",
                unsafe_allow_html=True
            )

            # Alternativas, sem índice inicial definido
            resposta_selecionada = st.radio(
                "", 
                alternativas, 
                key=f'pergunta_{index}',
                label_visibility='collapsed'
            )

            respostas_usuario[pergunta] = resposta_selecionada

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
            
            # Armazenar o número de acertos no session_state
            st.session_state.acertos = acertos

            # Exibindo o resultado total
            st.success(f"Você acertou {st.session_state.acertos} de {len(perguntas_df)} perguntas.")

            # Mostrando feedback individual para cada pergunta
            for index, row in perguntas_df.iterrows():
                pergunta = row['pergunta']
                correta = row['correta']
                if respostas_usuario[pergunta] == correta:
                    st.write(f"{pergunta} - Correto! ✅")
                else:
                    st.write(f"{pergunta} - Incorreto ❌")
else:
    st.sidebar.warning("Por favor, selecione a disciplina e o número do questionário para continuar.")
