import streamlit as st

# from sqlalchemy import create_engine, text


st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/5.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("About")

st.write("# Ways to help the project")
st.info("Here you will find information on how to help the project")
st.caption(
    'This project is developed and maintained by only one person. Running this project requires resources to collect '
    'and store information. I am currently unemployed and this is the only way to provide a living for me and my '
    'family. Thank you.')

st.write('IBAN $: TR41 0013 4000 0210 3974 9000 02')
st.write('IBAN €: TR14 0013 4000 0210 3974 9000 03')
st.write('IBAN ₽: TR84 0013 4000 0210 3974 9000 04')

# query = """SELECT country AS country,
#        count(country) AS "COUNT(country)"
# FROM public.agencies
# GROUP BY country
# ORDER BY "COUNT(country)" DESC
# LIMIT 100;"""
