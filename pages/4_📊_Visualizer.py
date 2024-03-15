import streamlit as st
from scripts.utils import AsmiService
from scripts.interface import draw_sidebar
from scripts.interface import draw_today

# from scripts.constants import categories_dict

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/4.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("Visualizer")

st.write("# Visualizer")
st.info("""Here yoy can find some graphs about the structure of Russian media and news flow""")
# st.divider()

news_amount_selection, category_selection, agency_selection = draw_sidebar()

agency_types = ['State', 'Independents', 'Foreign']
agencies_types_dict = {'State': '💀️', 'Independents': '🐈', 'Foreign': '👽'}

translator_selections = {agency_types[type]: agency_selection[type] for type in range(len(agency_types))}
selected_categories = [type for type in agency_types if translator_selections[type]]

columns_amount = len(selected_categories)
match columns_amount:
    case 0:
        pass
    case 1:
        pass
    case _:
        columns = st.columns(columns_amount)
        for i, column in enumerate(columns):
            news_service = AsmiService(service_name='asmi_media_type', media_type=selected_categories[i],
                                       news_amount=news_amount_selection, categories=category_selection)
            with column:
                agency_type = selected_categories[i]
                agency_emoj = agencies_types_dict[agency_type]
                column.header(agency_emoj + ' ' + agency_type)
                draw_today(news_service)

# news_service = AsmiService(service_name='asmi_media_type', media_type='Independents', news_amount=news_amount_selection,
#                            categories=category_selection)
#
# draw_today(news_service)
