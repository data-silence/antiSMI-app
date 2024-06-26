"""
Functions for creating individual interface elements.
The name of the function corresponds to its purpose in the application
"""

import streamlit as st
import extra_streamlit_components as stx

import datetime as dt
from dateutil.relativedelta import relativedelta

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import pymorphy2

from src.constants import tm_start_date, tm_last_date, major_events, categories_dict, media_types_dict, stop_words
from src.scripts import select_random_date, pymorphy2_311_hotfix
from src.services import AsmiService, TimemachineService

"""
Common selectors
"""


def draw_toggle(category_list: list) -> list:
    category_selection = [st.sidebar.toggle(category, value=True) for category in category_list]
    zip_dict = {el[0]: el[1] for el in zip(category_list, category_selection)}
    categories_selection = [category for category, is_presence in zip_dict.items() if is_presence]
    return categories_selection


def draw_media_types_selection() -> list:
    st.sidebar.caption('Media types')
    media_types = [media for media in media_types_dict]
    media_selection = draw_toggle(media_types)
    media_selection = [media.title() for media in media_selection]
    return media_selection


def draw_categories_selection() -> list:
    st.sidebar.caption('Categories')
    categories_types = [category for category in categories_dict]
    categories_selection = draw_toggle(categories_types)
    return categories_selection


"""
Sidebar
"""


def draw_sidebar(page_name: str) -> tuple | bool:
    st.sidebar.header("Pickup news you want:")
    news_amount_selection = st.sidebar.slider('News amount', 1, 10, 3)

    match page_name:
        case 'Nowadays':
            media_selection = draw_media_types_selection()
            categories_selection = draw_categories_selection()

            if not media_selection or not categories_selection:
                return False

            return news_amount_selection, categories_selection, media_selection

        case _:
            categories_selection = draw_categories_selection()

            if not categories_selection:
                return False

            return news_amount_selection, categories_selection


def write_contact():
    st.sidebar.header("Contact:")
    st.sidebar.markdown(':writing_hand: [@data_silence](https://t.me/data_silence)')
    st.sidebar.markdown(':mailbox_with_no_mail: enjoy-ds@pm.me')
    st.sidebar.markdown(':hammer_and_wrench:️ [Github](https://github.com/data-silence)')


"""
News representations
"""


def draw_single_news(all_news: list, painter) -> None:
    for news in all_news:
        painter.write(news[0].time())
        painter.write(news[1])
        painter.caption(news[2])
        links_list = news[3].split(' ')
        source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
        capt = painter.expander("...", False)
        capt.caption(f'sources & related: {source_links}', unsafe_allow_html=True)


@st.cache_resource
def draw_digest(news_service: AsmiService | TimemachineService, mode: str = 'single') -> None:
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
        case 'compare':
            if selected_categories:
                painter = st
                compared_category = selected_categories[0]
                draw_single_news(user_news_dict[compared_category], painter)


@st.cache_data
def draw_word_cloud(temp_df: pd.DataFrame) -> None:
    pymorphy2_311_hotfix()
    morph = pymorphy2.MorphAnalyzer()

    words = temp_df.title.str.split(' ').explode().values
    words = [morph.parse(word)[0].normal_form for word in words if morph.parse(word)[0].normal_form not in stop_words]

    wc = WordCloud(background_color="black", width=1600, height=800)
    wc.generate(" ".join(words))

    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    plt.axis("off")
    plt.tight_layout(pad=0)
    ax.set_title(f"Picture of the day", fontsize=30)
    ax.imshow(wc, alpha=0.98)
    st.pyplot(fig)


"""
Nowadays main page
"""


def draw_nowadays_tab1(news_amount_selection: int, category_selection: list, media_selection: list) -> None:
    news_service = AsmiService()
    news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                            media_type=media_selection)
    with st.expander("Picture of the day as a tag's cloud - expand to see..."):
        draw_word_cloud(news_service.date_df)
    draw_digest(news_service, mode='single')


def draw_nowadays_tab2(news_amount_selection: int, category_selection: list, media_selection: list) -> None:
    try:
        news_service = AsmiService(date_mode='precision')
        news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                media_type=media_selection)
        with st.expander("Picture of the day as a tag's cloud - expand to see..."):
            draw_word_cloud(news_service.date_df)
        draw_digest(news_service, mode='single')
    except KeyError:
        st.error("The morning news has not yet been compiled, make an enquiry after 10am.")


def draw_nowadays_tab3(news_amount_selection: int) -> None:
    with st.expander("This mode doesn't work the way you might expect it to work. Click to learn more"):
        st.error('1. In this mode you can only configure the number of news items and the category below. '
                 'Other settings from the sidebar do not affect the result. ')
        st.error('2. This mode does not show all news: neutral and non-political resources are not represented')
    news_service = AsmiService()
    comparison_categories = st.radio(
        "Choose a category to compare:",
        ['economy', 'society', 'entertainment'],
        horizontal=True, index=0
    )
    comparison_category = [comparison_categories]
    # comparison_media = [media.title() for media in media_types_dict]
    comparison_media = [media for media in news_service.date_df.media_type.value_counts().index.tolist() if
                        media not in ["Neutral", "Non-political"]]

    columns_amount = len(comparison_media)
    columns = st.columns(columns_amount)

    for i, column in enumerate(columns):
        user_media = [comparison_media[i]]
        news_service.set_params(news_amount=news_amount_selection, categories=comparison_category,
                                media_type=user_media)
        with column:
            agency_type = comparison_media[i]
            agency_emoj = media_types_dict[agency_type.lower()]
            column.header(agency_emoj + ' ' + agency_type)
            draw_digest(news_service, mode='compare')


"""
Timemachine main page
"""


def draw_timemachine_selector() -> tuple:
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


def draw_query_settings() -> tuple:
    st.sidebar.header("Search Settings:")
    years = st.sidebar.slider('Time frame', 1999, 2021, (1999, 2021))
    start_year = dt.datetime(years[0], 1, 1)
    end_year = dt.datetime(years[1], 12, 31)
    news_amount = st.sidebar.slider('News amount', 1, 100, 50)
    return start_year, end_year, news_amount


def draw_tm_tab(start_date: dt.date, end_date: dt.date, news_amount: int, categories: list) -> None:
    news_service = TimemachineService()
    news_service.set_params(start_date=start_date, end_date=end_date, news_amount=news_amount,
                            categories=categories)
    with st.expander("Picture of the day as a tag's cloud"):
        draw_word_cloud(news_service.date_df)
    with st.spinner('It takes about 30 seconds to fly in a time machine...'):
        draw_digest(news_service=news_service, mode='single')
