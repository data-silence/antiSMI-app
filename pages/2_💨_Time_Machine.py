import streamlit as st
from src.interface import draw_sidebar, draw_time_selector, draw_date_digest, draw_word_cloud
from src.scripts import TimemachineService

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/2.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

news_service = TimemachineService()

news_amount, categories = draw_sidebar('Time Machine')

try:
    if dates := draw_time_selector():
        start_date, end_date = dates
        with st.spinner('It takes about 30 seconds to fly in a time machine...'):
            draw_date_digest(news_service=news_service, start_date=start_date, end_date=end_date,
                             news_amount=news_amount, categories=categories)
        st.empty()
        st.subheader('Picture of the day:')
        draw_word_cloud(news_service.date_df)

except ValueError:
    st.error("Please complete date selection or categories selection")
