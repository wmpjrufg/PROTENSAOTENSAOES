"""Funções utilizadas no aplicativo"""
import pandas as pd

def carregando_dados():
    """
    Carrega os dados de um arquivo excel

    Args:
        None

    Returns:
        x (List): Lista com valores das coordenadas do eixo x (m)
        e_p (List): Lista com valores da excecentricidade de protensão (m)
    """
    data = pd.read_excel('Pasta1.xlsx', nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


def tensao_momento_g(w_t, w_b, delta_g, m_g):
    """Determina a tensão de flexão devido a uma lista de momentos devido a cargas permanentes.

    Args:
        w_t (float): Módulo plástico do topo da seção (m3)
        w_b (float): Módulo plástico da base da seção (m3)
        delta_g (List): Lista com valores da condição de existência da tensão na idade analisada (lista de booleano)
        m_g (List): Lista com valores do momento fletor (lista de float)        

    Returns:
        sigma_b_mg (float): Tensão de flexão na base devido ao momento fletor (kPa)
        sigma_t_mg (float): Tensão de flexão no topo devido ao momento fletor (kPa)
    """

    sigma_b_mg = 0
    sigma_t_mg = 0
    for i in range(len(delta_g)):
        sigma_b_mg += -delta_g[i] * m_g[i] / w_b
        sigma_t_mg += delta_g[i] * m_g[i] / w_t
    return sigma_b_mg, sigma_t_mg


def tensao_momento_q(w_t, w_b, i_c, delta_q, m_q):
    sigma_b_mq = 0
    sigma_t_mq = 0
    for i in range(len(delta_q)):
        sigma_b_mq += -delta_q[i] * m_q[i] * psi[i] / w_b
        sigma_t_mq += delta_q[i] * m_q[i] * psi[i] / w_t
    return sigma_b_mq, sigma_t_mq


def tensao_momento_p(A, w_t, w_b, i_c, e_p, delta_p, p_i):
    sigma_b_mp = 0
    sigma_t_mp = 0
    for i in range(len(delta_p)):
        sigma_b_mp += (delta_p[i] * p_i[i] / area) + ((delta_p[i] * p_i[i] * e_p) / w_b)
        sigma_t_mp += (delta_p[i] * p_i[i] / area) - ((delta_p[i] * p_i[i] * e_p) / w_t)
    return sigma_b_mp, sigma_t_mp

sigma_b_mg, sigma_t_mg = tensao_momento_g(w_t, w_b, i_c, delta_g, m_g)
print(sigma_b_mg, sigma_t_mg)

sigma_b_mq, sigma_t_mq = tensao_momento_q(w_t, w_b, i_c, delta_q, m_q)
print(sigma_b_mq, sigma_t_mq)

sigma_b_mp, sigma_t_mp = tensao_momento_p(area, w_t, w_b, i_c, e_p, delta_p, p_i)
print(sigma_b_mp, sigma_t_mp)

sigma_b_total = sigma_b_mg + sigma_b_mq + sigma_b_mp
sigma_t_total = sigma_t_mg + sigma_t_mq + sigma_t_mp
print(sigma_b_total, sigma_t_total)