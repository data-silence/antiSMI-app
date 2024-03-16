import streamlit as st
from src.constants import agencies_types_dict
from src.interface import draw_sidebar, draw_today_single_digest, draw_today_multi_digest
from src.scripts import AsmiService

st.set_page_config(
    page_title="Nowdays",
    page_icon="🗞️",
    layout="wide"
)

news_amount_selection, category_selection, media_selection = draw_sidebar('Now')

st.image('img/1.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# What is happening in Russia today and on the same day in the past?")

columns_amount = len(media_selection)
match columns_amount:
    case 0:
        st.error("Please select at least one media type from the sidebar settings menu")
    case 1:
        news_service = AsmiService(news_amount=news_amount_selection, categories=category_selection)
        draw_today_single_digest(news_service)
    case _:
        columns = st.columns(columns_amount)
        for i, column in enumerate(columns):
            news_service = AsmiService(service_name='asmi_media_type', media_type=media_selection[i],
                                       news_amount=news_amount_selection, categories=category_selection)
            with column:
                agency_type = media_selection[i]
                agency_emoj = agencies_types_dict[agency_type]
                column.header(agency_emoj + ' ' + agency_type)
                draw_today_multi_digest(news_service)
