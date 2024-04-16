import streamlit as st
from src.constants import media_types_dict, categories_dict
from src.interface import draw_sidebar, draw_word_cloud, draw_digest
from src.scripts import AsmiService

st.set_page_config(
    page_title="Nowadays",
    page_icon="🗞️",
    layout="wide"
)

st.image('img/1.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# What is happening in Russia today?")
st.divider()

if user_selection := draw_sidebar('Nowadays'):
    news_amount_selection, category_selection, media_selection = user_selection

    st.info(
        """Choose a mode to read today's news""")

    tab1, tab2, tab3 = st.tabs(["Last 24 hours", "Last fresh", "Comparison"])

    with tab1:
        news_service = AsmiService()
        news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                media_type=media_selection)
        with st.expander("Picture of the day as a tag's cloud - expand to see..."):
            draw_word_cloud(news_service.date_df)
        draw_digest(news_service, mode='single')

    with tab2:
        news_service = AsmiService(date_mode='precision')
        news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                media_type=media_selection)
        with st.expander("Picture of the day as a tag's cloud - expand to see..."):
            draw_word_cloud(news_service.date_df)
        draw_digest(news_service, mode='single')

    with tab3:
        st.error(
            'In this mode you can only configure the number of news items and the category below. '
            'Other settings from the sidebar do not affect the result')
        news_service = AsmiService()
        comparison_categories = st.radio(
            "Choose a category to compare:",
            [category for category in categories_dict],
            horizontal=True, index=0
        )
        comparison_category = [comparison_categories]
        comparison_media = [media.title() for media in media_types_dict]

        columns_amount = len(comparison_media)
        columns = st.columns(columns_amount)

        for i, column in enumerate(columns):
            user_media = [comparison_media[i]]
            news_service.set_params(news_amount=news_amount_selection, categories=comparison_category,
                                    media_type=user_media)
            with column:
                agency_type = comparison_media[i]
                agency_emoj = media_types_dict[agency_type.lower()]
                column.header(agency_emoj + ' ' + agency_type)
                draw_digest(news_service, mode='compare')
else:
    st.error("Please select at least one media type and category from the sidebar settings menu")