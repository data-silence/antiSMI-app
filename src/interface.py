"""
Functions for creating individual interface elements.
The name of the function corresponds to its purpose in the application
"""

import streamlit as st
import extra_streamlit_components as stx
from src.constants import tm_start_date, tm_last_date, major_events
from src.scripts import select_random_date
import datetime as dt
from src.scripts import AsmiService, TimemachineService
from src.constants import categories_dict, media_types_dict, stop_words
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
from dateutil.relativedelta import relativedelta


def draw_toggle(category_list: list) -> list:
    category_selection = [st.sidebar.toggle(category, value=True) for category in category_list]
    zip_dict = {el[0]: el[1] for el in zip(category_list, category_selection)}
    categories_selection = [category for category, is_presence in zip_dict.items() if is_presence]
    return categories_selection


def draw_sidebar(page_name: str) -> tuple | bool:
    st.sidebar.header("Pickup news you want:")
    news_amount_selection = st.sidebar.slider('News amount', 1, 10, 3)

    match page_name:
        case 'Now':
            st.sidebar.caption('Media types')
            media_types = [media for media in media_types_dict]
            media_selection = draw_toggle(media_types)
            media_selection = [media.title() for media in media_selection]

            st.sidebar.caption('Categories')
            categories_types = [category for category in categories_dict]
            categories_selection = draw_toggle(categories_types)

            if not media_selection or not categories_selection:
                return False

            return news_amount_selection, categories_selection, media_selection

        case _:
            st.sidebar.caption('Categories')
            categories_types = [category for category in categories_dict]
            categories_selection = draw_toggle(categories_types)

            return news_amount_selection, categories_selection


@st.cache_resource
def draw_digest(news_service: AsmiService | TimemachineService, mode: str = 'single'):
    user_news_dict = news_service.digest_dict()
    selected_categories = list(user_news_dict.keys())

    match mode:
        case 'single':
            category_columns = st.columns(len(user_news_dict))
            for i, column in enumerate(category_columns):
                category = selected_categories[i]
                emoj = categories_dict[category]['emoj']
                all_news = user_news_dict[category]
                column.subheader(emoj + ' ' + category.title())
                painter = column
                draw_single_news(all_news, painter)
        case 'multi':
            for category in selected_categories:
                st.subheader(category.title())
                all_news = user_news_dict[category]
                painter = st
                draw_single_news(all_news, painter)


def draw_single_news(all_news: list, painter) -> None:
    for news in all_news:
        painter.write(news[0].time())
        painter.write(news[1])
        painter.caption(news[2])
        links_list = news[3].split(' ')
        source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
        capt = painter.expander("...", False)
        capt.caption(f'sources & related: {source_links}', unsafe_allow_html=True)


def draw_time_selector():
    st.info(
        """This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")
    mode = st.radio(
        "Change the time machine mode:",
        ["today in past", "presets", "manual", "random"], horizontal=True
    )
    date_selection = (None, None)
    match mode:
        case "today in past":
            delta = st.slider('How many years ago?', min_value=1, max_value=24, value=20, step=1)
            today = dt.date.today()
            past_day = today - relativedelta(years=delta)
            date_selection = (past_day, past_day)
        case 'manual':
            date_selection = st.date_input("Choose a specific day or period of time no longer than a month: 🛸",
                                           (),
                                           tm_start_date,
                                           tm_last_date, key=date_selection)
            st.caption(
                "Available to fly in the range from 31 Aug 1999 to 31 Dec 2021. Fasten your seatbelts, and let's go!")
        case 'random':
            if st.button(label="Press me to flight random day in the past"):
                random_date = select_random_date()
                date_selection = (random_date, random_date)
            else:
                date_selection = ()
        case 'presets':
            st.divider()
            st.caption("Choose any event from this timeline. Swipe with the mouse wheel")
            chosen_id = stx.tab_bar(data=[stx.TabBarItemData(id=i, title="", description=el['description']) for i, el in
                                          enumerate(major_events)])
            try:
                chosen_id = int(chosen_id)
                date_selection = (major_events[chosen_id]['start_date'], major_events[chosen_id]['end_date'])
            except ValueError:
                date_selection = ()

    if date_selection != ():
        start_date, end_date = date_selection
        st.success(f"Your destination period: {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
    return date_selection


@st.cache_data
def draw_word_cloud(temp_df: pd.DataFrame):
    words = temp_df.title.str.split(' ').explode().values
    words = [word.lower() for word in words if word.lower() not in stop_words]

    wc = WordCloud(background_color="black", width=1600, height=800)
    wc.generate(" ".join(words))

    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    plt.axis("off")
    plt.tight_layout(pad=0)
    ax.set_title(f"Picture of the day", fontsize=30)
    ax.imshow(wc, alpha=0.98)
    st.pyplot(fig)


def draw_query_settings():
    st.sidebar.header("Search Settings:")
    years = st.sidebar.slider('Time frame', 1999, 2021, (1999, 2021))
    start_year = dt.datetime(years[0], 1, 1)
    end_year = dt.datetime(years[1], 12, 31)
    news_amount = st.sidebar.slider('News amount', 1, 100, 50)
    return start_year, end_year, news_amount
