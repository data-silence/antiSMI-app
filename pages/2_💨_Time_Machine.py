import datetime
import streamlit as st

# from urllib.error import URLError

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/tm.jpg', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("Pickup your news")
st.sidebar.caption('Media types')
agency_types = ['State', 'Independents', 'Foreign']
agency_selections = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign' else st.sidebar.toggle(agency) for
                     agency in agency_types]
st.sidebar.caption('Categories')
categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
category_selections = [st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category)
                       for category in categories]
# print(list(zip(categories, category_selections)))
st.sidebar.slider('News amount', 1, 10, 3)

st.markdown("# Time Machine")
st.info("""This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")
# st.divider()


flight_date = st.date_input(" 🛸", datetime.date(2014, 2, 20))
st.caption("Available to fly in the range from 28 August 2000 to 31 May 2021. Fasten your seatbelts, and let's go!")
