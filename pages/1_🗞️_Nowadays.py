import streamlit as st
from src.constants import media_types_dict
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
news_service = AsmiService()
st.divider()

st.caption("Choose whether you want to compare how different types of media cover today's events.")
is_comparison_mode = st.toggle('Comparison mode')

if user_selection := draw_sidebar('Now'):
    news_amount_selection, category_selection, media_selection = user_selection

    columns_amount = len(media_selection)
    match is_comparison_mode:
        case True:
            selected_media = (*media_selection, 'Non-political', 'Neutral')
            with st.expander("Picture of the day as a tag's cloud - expand to see..."):
                draw_word_cloud(news_service.date_df.loc[news_service.date_df['media_type'].isin(selected_media)])

            columns = st.columns(columns_amount)
            for i, column in enumerate(columns):
                user_media = [media_selection[i], 'Non-political', 'Neutral']
                news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                        media_type=user_media)
                with column:
                    agency_type = media_selection[i]
                    agency_emoj = media_types_dict[agency_type.lower()]
                    column.header(agency_emoj + ' ' + agency_type)
                    draw_digest(news_service, mode='multi')
        case False:
            news_service.set_params(news_amount=news_amount_selection, categories=category_selection,
                                    media_type=media_selection)

            with st.expander("Picture of the day as a tag's cloud - expand to see..."):
                draw_word_cloud(news_service.date_df)
            draw_digest(news_service, mode='single')
else:
    st.error("Please select at least one media type from the sidebar settings menu")
