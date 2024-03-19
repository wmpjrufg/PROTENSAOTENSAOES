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
    data = pd.read_excel('Pasta1.xlsx')
    lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)

    x = data['x (m)'].tolist()  
    e_p = data['e_p (m)'].tolist()  
    m_gpp = data['m_gpp (kNm)'].tolist()
    m_gex = data ['m_gex (kNm)'].tolist()
    m_q = data['m_q (kNm)'].tolist()  
    p_i = data['p_i (kN)'].tolist()  
    
    return x, e_p, m_gpp, m_gex, m_q, p_i



def tensao_momento(w_t, w_b, delta, m_s):
    """Determina a tensão de flexão devido a momento fletor informado.

    Args:
        w_t (Float): Módulo plástico do topo da seção (m3)
        w_b (Float): Módulo plástico da base da seção (m3)
        delta (Booleano): Condição de existência da tensão na idade analisada
        m_s (Float): Momento fletor na seção (kN.m)     

    Returns:
        sigma_b_ms (Float): Tensão de flexão na base devido ao momento fletor (kPa)
        sigma_t_ms (Float): Tensão de flexão no topo devido ao momento fletor (kPa)
    """

    # Calculando as tensões
    sigma_b_ms = -delta * m_s / w_b
    sigma_t_ms = delta * m_s / w_t

    return sigma_b_ms, sigma_t_ms


def tensao_protensao(a_c, w_t, w_b, e_p, delta, p_s):
    """Determina a tensão devido a protensão informada.
    
    Args:
        a_c (Float): Área da seção transversal (m2)
        w_t (Float): Módulo plástico do topo da seção (m3)
        w_b (Float): Módulo plástico da base da seção (m3)
        e_p (Float): Excentricidade de protensão (m)
        delta (Booleano): Condição de existência da tensão na idade analisada
        p_s (Float): Valor da protensão na seção (kN)
    
    Returns:
        sigma_b_mp (Float): Tensão de flexão na base devido a protensão (kPa)
        sigma_t_mp (Float): Tensão de flexão no topo devido a protensão (kPa)
    """

    # Calculando as tensões
    p_0 = delta * p_s / a_c
    p_1 = delta * p_s * e_p
    sigma_b_mp = p_0 + p_1 / w_b
    sigma_t_mp = p_0 - p_1 / w_t

    return sigma_b_mp, sigma_t_mp
