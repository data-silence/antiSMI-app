import streamlit as st
from sqlalchemy import create_engine, text



st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/7.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("About")

st.write("# The researcher's stories")
# st.divider()
st.info("Here you can find some stories related to my researching during the project work")

query = """SELECT country AS country,
       count(country) AS "COUNT(country)"
FROM public.agencies
GROUP BY country
ORDER BY "COUNT(country)" DESC
LIMIT 100;"""

