import streamlit as st

# from sqlalchemy import create_engine, text


st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('https://raw.githubusercontent.com/data-silence/banks-clients/master/img/bgr.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("About")

st.write("# Ways to help the project")
# st.info("Here you will find information on how to help the project")
st.info(
    'This project is developed and maintained by only one person. It requires a lot of time and at least $1,'
    '000 a month for servers and hosting. You can help to continue the project. Thank you.')

st.write('IBAN $: TR41 0013 4000 0210 3974 9000 02')
st.write('IBAN €: TR14 0013 4000 0210 3974 9000 03')
st.write('IBAN ₽: TR84 0013 4000 0210 3974 9000 04')

# query = """SELECT country AS country,
#        count(country) AS "COUNT(country)"
# FROM public.agencies
# GROUP BY country
# ORDER BY "COUNT(country)" DESC
# LIMIT 100;"""
