import streamlit as st

def footer():
    st.divider()

    st.text('Created by Justin Martin')

    col1, col2, col3 = st.columns([1, 1, 5])
    col1.link_button('LinkedIn', 'https://www.linkedin.com/in/justin-martin-40a680140/')
    col2.link_button('GitHub', 'https://github.com/jus10mar10')