import pandas as pd
import streamlit as st
from src.scripts import get_answer_df
from src.interface import draw_query_settings

st.set_page_config(
    page_title="LookUp",
    page_icon="🔎",
    layout="wide"
)

st.image('img/3.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Search answers in the past")

start_year, end_year, news_amount = draw_query_settings()

user_query = st.text_input(
    "Enter your question here 👇",
    label_visibility="collapsed",
    disabled=False,
    placeholder="Pick a search setting and input your question here...")

if user_query:
    with st.spinner('It takes about 30 seconds to find the answer in a 25 year news stream'):
        similar_news_df = get_answer_df(start_date=start_year, end_date=end_year, query=user_query)

    similar_news_df['year'] = similar_news_df['date'].apply(lambda x: x.year)

    data_frame = pd.DataFrame(similar_news_df['year'].value_counts(), columns=['count'])
    st.caption('Distribution of responses over time')
    st.bar_chart(data_frame, color='#ffaa0088')

    similar_news_df = similar_news_df.head(news_amount)
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
