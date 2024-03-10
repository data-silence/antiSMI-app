import streamlit as st
from scripts.utils import NewsService, categories_dict
from scripts.interface import draw_sidebar

st.set_page_config(
    page_title="Nowdays",
    page_icon="🗞️",
    layout="wide"
)

news_amount_selection, category_selection, agency_selection = draw_sidebar()

st.image('img/6.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Russian news for 25 years till nowadays")
st.info("What is happening in Russia today? What happened on the same day in the past?")


