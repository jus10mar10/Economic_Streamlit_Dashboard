import streamlit as st
from modules.footer import footer
from modules.cpi import get_cpi_index
import plotly.express as px

st.header("Page Under Construction")

@st.cache_data
def data_pull_cpi():
    """Fetches CPI data and caches it using streamlit cache."""
    data = get_cpi_index()
    return data

st.subheader("CPI All Urban Consumers (CPI-U) Index")

data = data_pull_cpi().sort_index(ascending=True) # cahce data changed order for some reason?
data['value'] = data['value'].astype(float)

annual_pct_change = data['value'].rolling(12).sum().pct_change(12).dropna()


col1, col2, col3 = st.columns(3)
cpi_data = st.checkbox("Show Data", value=False, key="cpi_data_checkbox")

if cpi_data:
    col1.text("Annual % Change")
    col1.write(annual_pct_change)
    col2.text("Previous Period % Change")
    col3.text("Index Values")
    
    
st.area_chart(annual_pct_change)

####################
footer()