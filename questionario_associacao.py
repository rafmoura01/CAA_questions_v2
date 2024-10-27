import streamlit as st
import pandas as pd
import random

# Carrega o CSV com as questões
questoes_df = pd.read_csv('questoes.csv', delimiter=';')  # use o delimitador correto, se necessário


# Filtra apenas as questões de associação
questoes_associacao = questoes_df[questoes_df['Tipo'] == 'Associacao']

# Loop para exibir cada questão de associação
for idx, row in questoes_associacao.iterrows():
    st.write(f"Questão {idx+1}: {row['Pergunta']}")
# Divide as associações (assumindo que o delimitador é ";")
    associacoes = [x.split("->") for x in row['Opções'].split(";")]
    itens_esquerda = [item.strip() for item, _ in associacoes]
    itens_direita = [desc.strip() for _, desc in associacoes]
 # Embaralha a lista da direita para tornar o desafio mais interessante
    random.shuffle(itens_direita)
    # Dicionário para armazenar as respostas do usuário
    respostas = {}
# Exibe os itens da esquerda e permite que o usuário faça as associações com os itens da direita
    for item in itens_esquerda:
        resposta = st.selectbox(f"Associe '{item}' com:", itens_direita, key=f"{idx}_{item}")
        respostas[item] = resposta
# Avalia as respostas ao clicar no botão
    if st.button("Verificar Respostas", key=f"check_{idx}"):
        resposta_correta = dict(associacoes)  # converte a resposta correta para um dicionário
        acertos = sum(respostas[item] == resposta_correta[item] for item in respostas)

# Exibe feedback
        if acertos == len(respostas):
            st.success(f"Parabéns! Você acertou todas as associações da questão {idx+1}!")
        else:
            st.warning(f"Você acertou {acertos} de {len(respostas)} associações na questão {idx+1}. Tente novamente!")
