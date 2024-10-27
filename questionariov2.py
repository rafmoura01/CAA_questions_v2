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
        st.stop()  # Para o código aqui caso o arquivo não exista
    except pd.errors.EmptyDataError:
        st.error("O arquivo está vazio. Por favor, adicione perguntas.")
        st.stop()  # Para o código se o arquivo estiver vazio
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo CSV: {e}")
        st.stop()  # Para o código em caso de outro erro

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
    numero_questionario = st.sidebar.selectbox("Escolha o número do questionário:", ["Selecione..."] + list(range(1, 8)))
else:
    numero_questionario = None

# Verifica se a disciplina e o número do questionário foram escolhidos
if disciplina_escolhida != "Selecione..." and numero_questionario != "Selecione...":
    # Exibe o subtítulo com a disciplina escolhida e o número do questionário
    subtitulo = subtitulos_disciplinas.get(disciplina_escolhida, disciplina_escolhida)
    st.subheader(f"Disciplina: {subtitulo} | Questionário: {numero_questionario}")

    # Gerar o nome do arquivo CSV com base na disciplina e no número do questionário
    nome_arquivo = f"perguntas_{disciplinas[disciplina_escolhida]}_{numero_questionario}.csv"

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
