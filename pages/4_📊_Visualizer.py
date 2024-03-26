import streamlit as st

from src.graphs import draw_countries_pie, draw_cities_barchart, draw_top_charts
from src.scripts import get_df_from_asmi

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/4.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("Visualizer")

st.write("# Visualizer")
st.sidebar.success("""Here yoy can find some graphs and research about the structure of Russian media and news flow""")

df = get_df_from_asmi("/agencies/all")
yandex_news_tab, antiSMI_tab, fun_research_tab = st.tabs(['Yandex News', 'Anti SMI', 'Fun Research'])

with yandex_news_tab:
    st.info('This is graphs about Yandex News media agency partners on the eve of 2022')
    draw_countries_pie(df)
    st.divider()
    draw_cities_barchart(df)
    st.divider()
    draw_top_charts(df)

with antiSMI_tab:
    st.info('Here you will find a visualisation of the development of the AntiSMI project')

with fun_research_tab:
    st.info('Fun visualisations and research related to news studies will be posted here')