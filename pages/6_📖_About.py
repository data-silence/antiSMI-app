import streamlit as st

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/10.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# About project")
st.divider()
st.sidebar.header("About")

st.markdown(
    """
    AntiSMI project is a research and still non-profit project at the intersection of ML and journalism that uses 
    machine learning models to analyse changes in the news flow in real time, trying to create a fundamentally 
    different way of consuming news in modern society.
    
    The project started with collecting and analysing information about partners of Yandex-news service as of the 
    beginning of last peaceful summer 2021. 
    
    Due to stupid events around here, it keeps growing and changing and I have no control over it anymore. I don't know 
    when or how it will end.
    """
)