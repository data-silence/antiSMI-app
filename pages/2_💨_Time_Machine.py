import streamlit as st
from scripts.interface import draw_sidebar, draw_time_selector
from scripts.utils import categories_dict, NewsService
import datetime as dt

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/5.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

news_service = NewsService(service_name='timemachine')


def draw_date_digest(start_date: dt.date, end_date: dt.date, news_amount: int, categories: list[str]):
    # print(start_date, end_date, news_amount, categories)
    news_service.set_params(start_date=start_date, end_date=end_date, news_amount=news_amount, categories=categories)
    # print(news_service.date_df.columns)
    # print(news_service.most_df)

    user_news = news_service.digest_df()

    selected_categories = list(user_news.keys())
    category_columns = st.columns(len(user_news))

    for i, column in enumerate(category_columns):
        category = selected_categories[i]
        emoj = categories_dict[category]['emoj']
        all_news = user_news[category]
        column.subheader(emoj + ' ' + category.title())
        for news in all_news:
            # column.caption(news[0].time().isoformat(timespec='minutes'))
            column.write(news[0].time())
            column.write(news[1])
            # capt = column.expander("...", False)
            # column.caption('News resume:')
            column.caption(news[2])
            links_list = news[3].split(' ')
            source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
            capt = column.expander("...", False)
            # column.caption(f'sources & related: {source_links}', unsafe_allow_html=True)
            capt.caption(f'sources & related: {source_links}', unsafe_allow_html=True)


news_amount, categories, agency = draw_sidebar()

# print(draw_time_selector())
try:
    if dates := draw_time_selector():
        start_date, end_date = dates
        with st.spinner('It takes about 30 seconds to fly in a time machine...'):
            draw_date_digest(start_date=start_date, end_date=end_date, news_amount=news_amount, categories=categories)
except ValueError:
    st.error("Please complete date selection")
