import streamlit as st
from scripts.utils import get_df_from_handlers_response

st.set_page_config(
    page_title="Nowdays",
    page_icon="🗞️",
    layout="wide"
)

st.image('img/6.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Russian news for 25 years till nowadays")
st.info("What is happening in Russia today? What happened on the same day in the past?")
# st.divider()

st.sidebar.header("Pickup news you want:")
st.sidebar.slider('News amount', 1, 10, 3)
st.sidebar.caption('Media types')
agency_types = ['State', 'Independents', 'Foreign']
agency_selections = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign' else st.sidebar.toggle(agency) for agency in agency_types]
st.sidebar.caption('Categories')
categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
category_selections = [st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category) for category in categories]
# print(list(zip(categories, category_selections)))




df = get_df_from_handlers_response('last_quota')
st.dataframe(df, use_container_width=True)