# import datetime
import streamlit as st
from scripts.interface import draw_sidebar
from scripts.utils import tm_start_date, tm_last_date

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/5.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

news_amount_selection, category_selection, agency_selection = draw_sidebar()

st.info("""This a is time machine! It can throw you into the news stream of the past. Any day in the last 25 years.""")

date_selection = st.date_input("Choose a specific day or period of time no longer than a month: 🛸", (), tm_start_date,
                               tm_last_date)
st.caption("Available to fly in the range from 31 Aug 1999 to 31 Dec 2021. Fasten your seatbelts, and let's go!")
