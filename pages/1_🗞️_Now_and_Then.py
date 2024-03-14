import streamlit as st
from scripts.utils import AsmiService
from scripts.constants import categories_dict
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

news_service = AsmiService(news_amount=news_amount_selection, categories=category_selection)


def draw_date_digest():
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


draw_date_digest()
