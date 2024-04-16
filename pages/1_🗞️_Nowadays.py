import streamlit as st
from src.interface import draw_sidebar, draw_nowadays_tab1, draw_nowadays_tab2, draw_nowadays_tab3

st.set_page_config(
    page_title="Nowadays",
    page_icon="🗞️",
    layout="wide"
)

st.image('img/1.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# What is happening in Russia today?")
st.divider()

if user_selection := draw_sidebar('Nowadays'):
    news_amount_selection, category_selection, media_selection = user_selection

    st.info(
        """Choose a mode to read today's news""")

    tab1, tab2, tab3 = st.tabs(["Last 24 hours", "Last fresh", "Comparison"])

    with tab1:
        draw_nowadays_tab1(news_amount_selection, category_selection, media_selection)
    with tab2:
        draw_nowadays_tab2(news_amount_selection, category_selection, media_selection)
    with tab3:
        draw_nowadays_tab3(news_amount_selection)
else:
    st.error("Please select at least one media type and category from the sidebar settings menu")
