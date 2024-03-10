import streamlit as st
from scripts.interface import draw_sidebar
from scripts.utils import tm_start_date, tm_last_date, categories_dict, NewsService, select_random_date

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/5.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

random_date = select_random_date()
news_service = NewsService(service_name='timemachine', start_date=random_date, end_date=random_date)

news_amount, categories, agency = draw_sidebar()

st.info("""This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")


def show_timemachine():
    mode = st.radio(
        "Change the time machine mode if necessary:",
        ["manual", "random", "preset"], horizontal=True
    )
    st.divider()
    match mode:
        case 'manual':
            date_selection = st.date_input("Choose a specific day or period of time no longer than a month: 🛸", (),
                                           tm_start_date,
                                           tm_last_date)
            st.caption(
                "Available to fly in the range from 31 Aug 1999 to 31 Dec 2021. Fasten your seatbelts, and let's go!")
        case 'random':

            date_selection = (random_date, random_date)
        case 'preset':
            pass
    return date_selection


if data_selection := show_timemachine():
    start_date, end_date = data_selection

    news_service.set_params(start_date=start_date, end_date=end_date, news_amount=news_amount, categories=categories)

    st.success(f"{start_date.strftime('%d %b %Y')}-{end_date.strftime('%d %b %Y')}")

    my_news = news_service.digest_df()
    selected_categories = list(my_news.keys())

    columns = st.columns(len(my_news))

    for i, column in enumerate(columns):
        category = selected_categories[i]
        emoj = categories_dict[category]['emoj']
        all_news = my_news[category]
        column.subheader(emoj + ' ' + category.title())
        for news in all_news:
            column.caption(news[0].time().isoformat(timespec='minutes'))
            column.write(news[1])
            capt = column.expander("...", False)
            capt.caption('News resume:')
            capt.caption(news[2])
            links_list = news[3].split(',')
            sourse = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
            capt.caption(f'sources & related: {sourse}', unsafe_allow_html=True)
