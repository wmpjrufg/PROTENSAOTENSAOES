"""Aplicativo de verificação de tensões"""
import streamlit as st 
import pandas as pd 
import numpy as np

from protendido import *


# x = [1.98, 3.96, 5.94, 7.92, 9.90, 11.80, 13.86, 15.84, 17.82, 19.8] # vem do usuário
# e_p = [0.38] * 10 # vem do usuário
# m_gpp = [1] * 10 # vem do usuário
# m_gex = [1] * 10 # vem do usuário
# m_q = [1] * 10 # vem do usuário
# p_i = [1] * 10 # vem do usuário

html_text = """
<h1 style='color: blue;'>Título</h1>
<h2 style='color: green;'>Cabeçalho</h2>
<p>Lorem ipsum dolor sit amet. Qui voluptas odio ea blanditiis quae non numquam internos sed Quis repudiandae qui expedita sint.
Quo animi consectetur ea officia voluptate et delectus totam cum amet veniam! Non quod incidunt sed rerum vitae ea soluta libero.
Sit delectus quibusdam et nulla galisum sed esse assumenda.</p>
</a>
"""

# Renderizar o texto HTML
st.markdown(html_text, unsafe_allow_html=True)

# CHAMADA DA FUNÇÃO QUE CARREGA O ARQUIVO
x, e_p, m_gpp, m_gex, m_q, p_i = carregando_dados()


#IMPUTS DO USUARIO
# Lista de tuplas contendo o nome da variável
variaveis = [("a_c (m2):"), ("i_c (m4):"), ("w_t (m3):"), ("w_b (m3):")]

# Dicionário para armazenar os valores das variáveis
valores = {}

if None not in [x, e_p, m_gpp, m_gex, m_q, p_i]:
    # Pedindo ao usuário para inserir os valores correspondentes
    for nome in variaveis:
        valor_digitado = st.number_input(nome)
        if valor_digitado is not None and valor_digitado != 0:
            valores[nome[:-6]] = valor_digitado  # Atualiza o valor no dicionário apenas se o usuário digitou algo diferente de zero


    # Chamando as funções de cálculo dentro do botão
    if st.button("Calcular Tensões"):
        # Verifica se todas as chaves esperadas estão no dicionário
        chaves_faltando = [nome[:-6] for nome in variaveis if nome[:-6] not in valores]
        if chaves_faltando:
            st.error(f"Por favor, insira valores para as seguintes variáveis: {', '.join(chaves_faltando)}")
        else:
            # Atribuindo os valores das variáveis
            a_c = valores.get("a_c", 1)
            i_c = valores.get("i_c", 1)
            w_t = valores.get("w_t", 1)
            w_b = valores.get("w_b", 1)
            st.success("Valores adicionados com sucesso!")

            try:
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
                
                # Criando DataFrame com os resultados
                chart_data = pd.DataFrame({ 
                    'e_p': e_p,
                    'x (m)': x,
                    'm_gpp': m_gpp,
                    'm_gex': m_gex,
                    'm_q': m_q,
                    'p_i': p_i,
                    'sigma t t0': sigma_t_t0,
                    'sigma b t0': sigma_b_t0, 
                    'sigma t tinf': sigma_t_tinf,
                    'sigma b tinf': sigma_b_tinf,
                })

                # Exibindo DataFrame
                st.write(chart_data)
                st.title("GRAFICO 1")
                st.subheader("Topo")
                st.line_chart(chart_data.set_index('x (m)')['sigma t t0'])

                st.subheader("Baixo")
                st.line_chart(chart_data.set_index('x (m)')['sigma b t0'])

                st.title("GRAFICO 2")
                st.subheader("Topo")
                st.line_chart(chart_data.set_index('x (m)')['sigma t tinf'])

                st.subheader("Baixo")
                st.line_chart(chart_data.set_index('x (m)')['sigma b tinf'])
                # Chamando a função para criar o botão de download
                download_excel(chart_data)

            except TypeError:
                st.error("Por favor, insira valores para todas as variáveis necessárias para calcular as tensões.")

# #CARREGANDO O ARQUIVO EXEL
# def load_data(nrows):
#     data = pd.read_excel('Pasta1.xlsx', nrows=nrows)
#     lowercase = lambda x: str(x).lower()
#     data.rename(lowercase, axis='columns', inplace=True)
#     return data

# # Create a text element and let the reader know the data is loading.
# data_load_state = st.text('Loading data...')
# # Load 10,000 rows of data into the dataframe.
# data = load_data(10000)
# # Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')

# st.subheader('Base de Dados Inicial')
# st.write(data)




