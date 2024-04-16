import streamlit as st
from src.interface import draw_sidebar, draw_timemachine_selector, draw_word_cloud, draw_digest
from src.scripts import TimemachineService

st.set_page_config(page_title="Time machine", page_icon="💨", layout="wide")
st.image('img/2.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

news_service = TimemachineService()

news_amount, categories = draw_sidebar('Time Machine')

try:
    if dates := draw_timemachine_selector():
        start_date, end_date = dates
        news_service.set_params(start_date=start_date, end_date=end_date, news_amount=news_amount,
                                categories=categories)
        with st.expander("Picture of the day as a tag's cloud"):
            draw_word_cloud(news_service.date_df)
        with st.spinner('It takes about 30 seconds to fly in a time machine...'):
            draw_digest(news_service=news_service, mode='single')
except ValueError:
    st.error("Please complete date selection or categories selection")
