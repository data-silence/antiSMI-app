import pandas
import streamlit as st
from scripts.utils import get_answer
from scripts.interface import draw_query_settings

st.set_page_config(
    page_title="LookUp",
    page_icon="🔎",
    layout="wide"
)

st.image('img/8.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Search answers in the past")
st.info("👈 Pick a search setting & Ask your question 👇")

category, years, news_amount = draw_query_settings()

user_query = st.text_input(
    "Enter your question here 👇",
    label_visibility="collapsed",
    disabled=False,
    placeholder="Enter your question here...")

if user_query:
    similar_news_df = get_answer(user_query)
    similar_news_df['year'] = similar_news_df['date'].apply(lambda x: x.year)
    similar_news_dict = {}

    for y in similar_news_df.year.unique():
        year_df = similar_news_df[similar_news_df.year == y]
        year_list = list(
            zip(year_df['date'], year_df['title'], year_df['resume'], year_df['links']))
        similar_news_dict.update({int(y): year_list})

    selected_years = list(sorted(similar_news_dict.keys()))

    for i, year in enumerate(selected_years):
        st.subheader(year)
        capt = st.expander("...", True)
        for news in similar_news_dict[year]:

            capt.write(news[1])
            capt.caption(news[2])
            links_list = news[3].split(' ')
            source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
            capt.caption(f'timestamp: [{news[0]}], sources & related: {source_links}', unsafe_allow_html=True)
