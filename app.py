import streamlit as st 
import pandas as pd 
import numpy as np
import random

sigma_b = [random.uniform(10000, 15000) for _ in range(10)]
sigma_t = [random.uniform(10000, 15000) for _ in range(10)]
x = [1.98, 3.96, 5.94, 7.92, 9.90, 11.80, 13.86, 15.84, 17.82, 19.8]

chart_data1 = pd.DataFrame(({'m': x, 'sigma b': sigma_b}))
chart_data2 = pd.DataFrame(({'m': x, 'sigma b': sigma_t}))
st.line_chart(chart_data1)
st.line_chart(chart_data2)