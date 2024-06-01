import streamlit as st

from src.interface import write_contact

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

write_contact()

st.image('https://raw.githubusercontent.com/data-silence/banks-clients/master/img/bgr.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Ways to help the project")

st.info(
    'It takes time and money to maintain the services. You can help to continue the project:')

st.write('IBAN $: TR41 0013 4000 0210 3974 9000 02')
st.write('IBAN €: TR14 0013 4000 0210 3974 9000 03')
st.write('IBAN ₽: TR84 0013 4000 0210 3974 9000 04')

st.info(
    'Thank you 💓')