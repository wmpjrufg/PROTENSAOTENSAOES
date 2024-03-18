"""Aplicativo de verificação de tensões"""
import streamlit as st 
import pandas as pd 
import numpy as np
import random


x = [1.98, 3.96, 5.94, 7.92, 9.90, 11.80, 13.86, 15.84, 17.82, 19.8]
e_p = [0.38] * 10 
sigma_b = []
sigma_t = []

# Pedindo para o usuário inserir elementos
a_c = st.number_input("a_c:")

i_c = st.number_input("i_c:")

w_t = st.number_input("w_t:")

w_c = st.number_input("w_c:")

tensao = random.uniform(10000, 15000)

for id, ep_x in enumerate(e_p):
    sigma_aux_b, sigma_aux_t = tensao(ep_x, a_c, i_c, w_t, w_c)
    sigma_b.append(sigma_aux_b)
    sigma_t.append(sigma_aux_t)


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