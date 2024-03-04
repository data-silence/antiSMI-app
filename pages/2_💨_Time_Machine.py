import datetime
import streamlit as st

# from urllib.error import URLError

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/5.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("Pickup news you want:")
st.sidebar.slider('News amount', 1, 10, 3)
st.sidebar.caption('Media types')
agency_types = ['State', 'Independents', 'Foreign']
agency_selections = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign' else st.sidebar.toggle(agency) for
                     agency in agency_types]
st.sidebar.caption('Categories')
categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
category_selections = [st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category)
                       for category in categories]
# print(list(zip(categories, category_selections)))
# if 'Society':
#     st.toast('Выбор этой категории не доступен бесплатным пользователям.')
#     # 'Society'(value=False)
# print(type('Society'))
if category_selections[3]:
    st.toast('Выбор этой категории не доступен бесплатным пользователям.')




# st.markdown("# Time Machine")
st.info("""This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")
# st.divider()

tm_start_date = datetime.date(1999, 8, 31)
tm_last_date = datetime.date(2023, 12, 31)
krym_start_date = datetime.date(2014, 2, 22)
krym_end_date = datetime.date(2014, 3, 26)
flight_date = st.date_input("Choose a specific day or period of time no longer than a month: 🛸", (), tm_start_date, tm_last_date)
st.caption("Available to fly in the range from 31 Aug 1999 to 31 Dec 2021. Fasten your seatbelts, and let's go!")

flight_date