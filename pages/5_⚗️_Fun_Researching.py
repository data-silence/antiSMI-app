import streamlit as st

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/2.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("About")

st.write("# The researcher stories")
# st.divider()
st.info("Here you can find some stories related to my researching during the project work")

