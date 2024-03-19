"""Aplicativo de verificação de tensões"""
import streamlit as st 
import pandas as pd 
import numpy as np

from protendido import *

# Chamando a função e atribuindo os valores retornados a variáveis
x, e_p, m_gpp, m_gex, m_q, p_i = carregando_dados()
# x = [1.98, 3.96, 5.94, 7.92, 9.90, 11.80, 13.86, 15.84, 17.82, 19.8] # vem do usuário
# e_p = [0.38] * 10 # vem do usuário
# m_gpp = [1] * 10 # vem do usuário
# m_gex = [1] * 10 # vem do usuário
# m_q = [1] * 10 # vem do usuário
# p_i = [1] * 10 # vem do usuário

# Lista de tuplas contendo o nome da variável e seu valor padrão
variaveis = [("a_c (m2):", 1.00), ("i_c (m4):", 1.00), ("w_t (m3):", 1.00), ("w_b (m3):", 1.00)]

# Dicionário para armazenar os valores das variáveis
valores = {}

# Pedindo ao usuário para inserir os valores correspondentes
for nome, valor_padrao in variaveis:
    valor_digitado = st.number_input(nome, value=valor_padrao)
    if valor_digitado != "":
        valores[nome[:-1]] = valor_digitado  # Atualiza o valor no dicionário apenas se o usuário digitou algo

# Atribuindo os valores das variáveis
a_c = valores.get("a_c (m2)", 1)
i_c = valores.get("i_c (m4)", 1)
w_t = valores.get("w_t (m3)", 1)
w_b = valores.get("w_b (m3)", 1)


# Determinando as tensões no Estado Vazio
sigma_b_t0 = []
sigma_t_t0 = []
for id, ep_x in enumerate(e_p):
    sigma_mg_b, sigma_mg_t = tensao_momento(w_t, w_b, 1, m_gpp[id])
    sigma_mq_b, sigma_mq_t = tensao_momento(w_t, w_b, 0, m_q[id])
    sigma_pi_b, sigma_pi_t = tensao_protensao(a_c, w_t, w_b, ep_x, 1, p_i[id])
    sigma_b_t0.append(sigma_mg_b + sigma_mq_b + sigma_pi_b)
    sigma_t_t0.append(sigma_mg_t + sigma_mq_t + sigma_pi_t)


# Determinando as tensões no Estado Limite de Serviço
sigma_b_tinf = []
sigma_t_tinf = []
for id, ep_x in enumerate(e_p):
    sigma_mg_b, sigma_mg_t = tensao_momento(w_t, w_b, 1, m_gpp[id]+m_gex[id])
    sigma_mq_b, sigma_mq_t = tensao_momento(w_t, w_b, 1, m_q[id])
    sigma_pi_b, sigma_pi_t = tensao_protensao(a_c, w_t, w_b, ep_x, 1, p_i[id])
    sigma_b_tinf.append(sigma_mg_b + sigma_mq_b + sigma_pi_b)
    sigma_t_tinf.append(sigma_mg_t + sigma_mq_t + sigma_pi_t)


#DATAFRAME 
chart_data = pd.DataFrame({
                            'sigma t t0': sigma_t_t0,
                            'sigma b t0': sigma_b_t0, 
                            'sigma t tinf': sigma_t_tinf,
                            'sigma b tinf': sigma_b_tinf, 
                            'm': x, 
                            'p_i': p_i,
                            'm_gpp': m_gpp,
                            'm_gex': m_gex,
                            'm_q': m_q,
                            })
chart_data

#CARREGANDO O ARQUIVO EXEL
def load_data(nrows):
    data = pd.read_excel('Pasta1.xlsx', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

st.subheader('Base de Dados Inicial')
st.write(data)

# Chamando a função e atribuindo os valores retornados a variáveis
x, e_p, m_gpp, m_gex, m_q, p_i = carregando_dados()


st.title("GRAFICO 1")
st.subheader("Topo")
st.line_chart(chart_data.set_index('m')['sigma t t0'])

st.subheader("Baixo")
st.line_chart(chart_data.set_index('m')['sigma b t0'])

st.title("GRAFICO 2")
st.subheader("Topo")
st.line_chart(chart_data.set_index('m')['sigma t tinf'])

st.subheader("Baixo")
st.line_chart(chart_data.set_index('m')['sigma b tinf'])