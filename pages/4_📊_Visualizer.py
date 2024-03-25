import streamlit as st

from src.graphs import draw_countries_type_pie, draw_countries_pie, draw_region_barchart
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
st.info("""Here yoy can find some graphs about the structure of Russian media and news flow""")
# st.divider()

df = get_df_from_asmi("/agencies/all")
# st.dataframe(df)
# df.query("category==country" & "category != ''")
selected_countries_types = st.radio(
    "",
    ['Exclude Russia', 'With Russia'],
    horizontal=True
)

st.write('Russian-language media by country')
draw_countries_type_pie(df, filter=selected_countries_types)


selected_countries = st.radio(
    "",
    ['Russian', 'Ukranian', 'Non Ukranian'],
    horizontal=True
)
draw_countries_pie(df=df, country=selected_countries)

selected_region = st.radio(
    "",
    ['Russian', 'Ukranian'],
    horizontal=True
)
draw_region_barchart(df=df, country=selected_region)

