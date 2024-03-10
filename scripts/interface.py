import streamlit as st
from scripts.utils import tm_start_date, tm_last_date, select_random_date


def draw_sidebar():
    st.sidebar.header("Pickup news you want:")
    news_amount_selection = st.sidebar.slider('News amount', 1, 10, 3)
    st.sidebar.caption('Media types')
    agency_types = ['State', 'Independents', 'Foreign']
    agency_selection = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign'
                        else st.sidebar.toggle(agency) for agency in agency_types]
    st.sidebar.caption('Categories')
    categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
    category_selection = [
        st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category)
        for category in categories]
    if category_selection[3]:
        st.toast('Выбор этой категории не доступен бесплатным пользователям.')
    zip_dict = {el[0]: el[1] for el in zip(categories, category_selection)}
    categories_selection = [k.lower() for k, v in zip_dict.items() if v]

    return news_amount_selection, categories_selection, agency_selection


def draw_time_selector():
    st.info(
        """This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")
    mode = st.radio(
        "Change the time machine mode if necessary:",
        ["manual", "random", "preset"], horizontal=True
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
            if st.button(label="Press to flight past random day"):
                random_date = select_random_date()
                date_selection = (random_date, random_date)
            else:
                st.error("Please press the button")
                date_selection = ()
        case 'preset':
            pass
    print(date_selection)
    if date_selection != ():
        start_date, end_date = date_selection
        st.success(f"{start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}")
    return date_selection
