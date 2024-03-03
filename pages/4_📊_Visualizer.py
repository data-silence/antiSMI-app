import streamlit as st

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/2.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("Visualizer")

st.write("# Visualizer")
st.info("""Here yoy can find some graphs about the structure of Russian media and news flow""")
# st.divider()


