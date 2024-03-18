import streamlit as st 
import pandas as pd 
import numpy as np
import random

sigma_b = [random.uniform(10000, 15000) for _ in range(10)]
sigma_t = [random.uniform(10000, 15000) for _ in range(10)]
x = [1.98, 3.96, 5.94, 7.92, 9.90, 11.80, 13.86, 15.84, 17.82, 19.8]

chart_data = pd.DataFrame({'sigma t': sigma_t,'sigma b': sigma_b, 'm': x})

st.title("GRAFICOS")
st.subheader("Topo")
st.line_chart(chart_data.set_index('m')['sigma t'])

st.subheader("Baixo")
st.line_chart(chart_data.set_index('m')['sigma b'])