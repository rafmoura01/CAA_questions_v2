import os
import streamlit as st
import pandas as pd
import requests
from io import StringIO

# Título do aplicativo
st.title("Bora passar na prova, Lateral!! 😄")

# Instruções
st.write("Por favor, escolha uma disciplina e o número do questionário no menu lateral.")

# URL da imagem no GitHub
imagem_caminho = "https://raw.githubusercontent.com/rafmoura01/CAA_questions_v2/main/Image_sgt.jpg"

# Dicionário com os textos personalizados para cada disciplina
subtitulos_disciplinas = {
    "CAO": "Características Organizacionais",
    "GP": "Gestão de Projetos",
    "GPC": "Gestão Patrimonial",
    "LE": "Liderança e Equipes",
    "PAI": "Processos Avaliativos e Inovação"
}

# Função para carregar o arquivo CSV com as perguntas a partir de uma URL do GitHub
def carregar_perguntas(url_csv):
    try:
        response = requests.get(url_csv)
        response.raise_for_status()  # Verifica se a requisição teve sucesso
        # Lê o conteúdo diretamente em um DataFrame
        df = pd.read_csv(StringIO(response.text), encoding='utf-8', sep=';')
        df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
        return df
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao baixar o arquivo CSV: {e}")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("O arquivo está vazio. Por favor, adicione perguntas.")
        st.stop()
    except pd.errors.ParserError as e:
        st.error(f"Erro ao analisar o arquivo CSV: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()

# Função para identificar os números de questionários disponíveis no GitHub
def obter_numeros_questionarios(disciplina_abreviacao):
    # URL da API GitHub para listar conteúdo do diretório
    url = "https://api.github.com/repos/rafmoura01/CAA_questions_v2/contents/"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição teve sucesso
        arquivos = response.json()  # Obtém a lista de arquivos como JSON
        
        # Filtra os arquivos com base na disciplina e no formato .csv
        numeros = [
            int(arquivo['name'].split('_')[-1].split('.')[0])
            for arquivo in arquivos
            if arquivo['name'].startswith(f"perguntas_{disciplina_abreviacao}_") and arquivo['name'].endswith(".csv")
        ]
        return sorted(numeros)
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao acessar o repositório do GitHub: {e}")
        return []

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

# Inserir a imagem na área do menu lateral, abaixo do seletor de questionário
st.sidebar.image(imagem_caminho, caption="Boa sorte no seu estudo!", use_column_width=True)

# Verifica se a disciplina e o número do questionário foram escolhidos
if disciplina_escolhida != "Selecione..." and numero_questionario != "Selecione...":
    # Exibe o subtítulo com a disciplina escolhida e o número do questionário
    subtitulo = subtitulos_disciplinas.get(abreviacao, disciplina_escolhida)
    st.subheader(f"Disciplina: {subtitulo} | Questionário: {numero_questionario}")

    # Gerar o URL do arquivo CSV com base na disciplina e no número do questionário
    nome_arquivo = f"https://raw.githubusercontent.com/rafmoura01/CAA_questions_v2/main/perguntas_{abreviacao}_{numero_questionario}.csv"
    
    # Mostrar a URL para verificação
    st.write("URL do CSV:", nome_arquivo)

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
