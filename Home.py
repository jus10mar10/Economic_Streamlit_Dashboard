import streamlit as st
from modules.footer import footer

st.title('Economic Dashboard')

col1, col2, col3 = st.columns([2, 2, 2])
col1.metric('Inflation Rate', .0000, delta=0.0)
col2.metric('Unemployment Rate', 0.0, delta=0.0)
col3.metric('GDP Growth Rate', 0.0, delta=0.0)
st.text('Annual Rates change from previous year')

####################
footer()