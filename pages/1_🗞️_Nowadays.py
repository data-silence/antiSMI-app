import streamlit as st
from src.constants import agencies_types_dict
from src.interface import draw_sidebar, draw_word_cloud, draw_digest
from src.scripts import AsmiService

st.set_page_config(
    page_title="Nowadays",
    page_icon="🗞️",
    layout="wide"
)

news_amount_selection, category_selection, media_selection = draw_sidebar('Now')

st.image('img/1.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# What is happening in Russia today?")

news_service = AsmiService()
columns_amount = len(media_selection)

match columns_amount:
    case 0:
        st.error("Please select at least one media type from the sidebar settings menu")
    case 1:
        news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                media_type=media_selection)

        with st.expander("Picture of the day as a tag's cloud - expand to see..."):
            draw_word_cloud(news_service.date_df)
        draw_digest(news_service, mode='single')
    case _:
        selected_media = (*media_selection, 'Non-political', 'Neutral')
        with st.expander("Picture of the day as a tag's cloud - expand to see..."):
            draw_word_cloud(news_service.date_df.loc[news_service.date_df['media_type'].isin(selected_media)])

        columns = st.columns(columns_amount)
        for i, column in enumerate(columns):
            news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                    media_type=media_selection[i])
            with column:
                agency_type = media_selection[i]
                agency_emoj = agencies_types_dict[agency_type]
                column.header(agency_emoj + ' ' + agency_type)
                draw_digest(news_service, mode='multi')
