import streamlit as st
import extra_streamlit_components as stx
from scripts.constants import tm_start_date, tm_last_date, major_events
from scripts.utils import select_random_date
import datetime as dt
from scripts.utils import AsmiService, TimemachineService
from scripts.constants import categories_dict


def draw_sidebar():
    st.sidebar.header("Pickup news you want:")
    news_amount_selection = st.sidebar.slider('News amount', 1, 10, 3)
    st.sidebar.caption('Media types')
    agency_types = ['State', 'Independents', 'Foreign']
    agency_selection = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign'
                        else st.sidebar.toggle(agency) for agency in agency_types]
    st.sidebar.caption('Categories')
    categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query

    category_selection = [st.sidebar.toggle(category, value=True) for category in categories]

    # category_selection = [
    #     st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category)
    #     for category in categories]
    # if category_selection[3]:
    #     st.toast('Выбор этой категории не доступен бесплатным пользователям.')
    zip_dict = {el[0]: el[1] for el in zip(categories, category_selection)}
    categories_selection = [k.lower() for k, v in zip_dict.items() if v]

    return news_amount_selection, categories_selection, agency_selection


def draw_today_single_digest(news_service: AsmiService):
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
            column.caption(news[2])
            links_list = news[3].split(' ')
            source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
            capt = column.expander("...", False)
            capt.caption(f'sources & related: {source_links}', unsafe_allow_html=True)


def draw_today_multi_digest(news_service: AsmiService):
    user_news_dict = news_service.digest_df()
    selected_categories = list(user_news_dict.keys())

    for category in selected_categories:
        st.subheader(category.title())
        all_news = user_news_dict[category]
        for news in all_news:
            st.write(news[0].time())
            st.write(news[1])
            capt = st.expander("...", False)

            capt.caption(news[2])
            links_list = news[3].split(' ')
            source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]

            capt.caption(f'sources & related: {source_links}', unsafe_allow_html=True)


def draw_time_selector():
    st.info(
        """This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")
    mode = st.radio(
        "Change the time machine mode:",
        ["preset", "manual", "random"], horizontal=True
    )
    date_selection = (None, None)
    match mode:
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
        case 'preset':
            st.divider()
            st.caption("Choose any event from this timeline. Swipe with the mouse wheel")
            chosen_id = stx.tab_bar(data=[
                stx.TabBarItemData(id=1, title="", description="Yeltsin's resignation"),
                stx.TabBarItemData(id=2, title="", description="President Putin"),
                stx.TabBarItemData(id=3, title="", description="Kursk"),
                stx.TabBarItemData(id=4, title="", description="September 11"),
                stx.TabBarItemData(id=5, title="", description="Nord-Ost"),
                stx.TabBarItemData(id=6, title="", description="Yukos case"),
                stx.TabBarItemData(id=7, title="", description="Orange Revolution"),
                stx.TabBarItemData(id=8, title="", description="Medvedev as Preemnik"),
                stx.TabBarItemData(id=9, title="", description="Georgian war"),
                stx.TabBarItemData(id=10, title="", description="Putin's back"),
                stx.TabBarItemData(id=11, title="", description="Bolotnaya rallies"),
                stx.TabBarItemData(id=12, title="", description="Million Man March"),
                stx.TabBarItemData(id=13, title="", description="Annexation of Crimea"),
            ])

            try:
                chosen_id = int(chosen_id)
                date_selection = (major_events[chosen_id]['start_date'], major_events[chosen_id]['end_date'])
            except ValueError:
                date_selection = ()

    if date_selection != ():
        start_date, end_date = date_selection
        st.success(f"Your destination period: {start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
    return date_selection


def draw_date_digest(news_service: TimemachineService, start_date: dt.date, end_date: dt.date, news_amount: int,
                     categories: list[str]):
    news_service.set_params(start_date=start_date, end_date=end_date, news_amount=news_amount, categories=categories)

    user_news = news_service.digest_df()

    selected_categories = list(user_news.keys())
    category_columns = st.columns(len(user_news))

    for i, column in enumerate(category_columns):
        category = selected_categories[i]
        emoj = categories_dict[category]['emoj']
        all_news = user_news[category]
        column.subheader(emoj + ' ' + category.title())
        for news in all_news:
            column.write(news[0].time())
            column.write(news[1])
            column.caption(news[2])
            links_list = news[3].split(' ')
            source_links = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
            capt = column.expander("...", False)
            capt.caption(f'sources & related: {source_links}', unsafe_allow_html=True)


def draw_query_settings():
    st.sidebar.header("Search Settings:")
    categories = ['economy', 'science', 'technology', 'society', 'entertainment', 'sports']
    category = st.sidebar.radio("Category", categories, horizontal=True, index=3)
    years = st.sidebar.slider('Time frame', 1999, 2021, (1999, 2021))
    start_year = dt.datetime(years[0], 1, 1)
    end_year = dt.datetime(years[1], 12, 31)
    news_amount = st.sidebar.slider('News amount', 1, 100, 50)
    return start_year, end_year, news_amount, category
