"""Aplicativo de verificação de tensões em peças protendidas"""
import streamlit as st
import pandas as pd
import numpy as np

from protendido import *

html_text = """
<h1 style='color: blue;'>Verificador de tensões de protensão em peças de concreto protendido</h1>
<p align="justify">
Lorem ipsum dolor sit amet. Qui voluptas odio ea blanditiis quae non numquam internos sed Quis repudiandae qui expedita sint.
Quo animi consectetur ea officia voluptate et delectus totam cum amet veniam! Non quod incidunt sed rerum vitae ea soluta libero.
Sit delectus quibusdam et nulla galisum sed esse assumenda.
</p>
"""

# Renderizar o cabeçalho HTML
st.markdown(html_text, unsafe_allow_html=True)

# Entrada de dados
variaveis = [("a_c (m2):"), ("i_c (m4):"), ("w_t (m3):"), ("w_b (m3):")]
x, e_p, m_gpp, m_gex, m_q, p_i = carregando_dados()

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
