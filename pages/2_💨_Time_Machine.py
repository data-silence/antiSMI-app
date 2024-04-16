import streamlit as st
from src.interface import draw_sidebar, draw_timemachine_selector, draw_tm_tab

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/2.png', use_column_width='auto',
         caption='Time Machine has an analogue in Telegram - @time_mashine_bot')

news_amount, categories = draw_sidebar('Time Machine')

try:
    if dates := draw_timemachine_selector():
        start_date, end_date = dates
        draw_tm_tab(start_date=start_date, end_date=end_date, news_amount=news_amount, categories=categories)

except ValueError:
    st.error("Please complete date selection or categories selection")
