"""Aplicativo de verificação de tensões"""
import streamlit as st 
import pandas as pd 
import numpy as np

from protendido import *


x = [1.98, 3.96, 5.94, 7.92, 9.90, 11.80, 13.86, 15.84, 17.82, 19.8] # vem do usuário
e_p = [0.38] * 10 # vem do usuário
m_gpp = [] # vem do usuário
m_gex = [] # vem do usuário
m_q = [] # vem do usuário
p_i = [] # vem do usuário

# Pedindo para o usuário inserir elementos
a_c = st.number_input("a_c (m2):")
i_c = st.number_input("i_c (m4):")
w_t = st.number_input("w_t (m3):")
w_b = st.number_input("w_b (m3):")

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
chart_data = pd.DataFrame({'sigma t': sigma_t,'sigma b': sigma_b, 'm': x})

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





st.title("GRAFICOS")
st.subheader("Topo")
st.line_chart(chart_data.set_index('m')['sigma t'])

st.subheader("Baixo")
st.line_chart(chart_data.set_index('m')['sigma b'])