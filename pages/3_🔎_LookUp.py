import streamlit as st

st.set_page_config(
    page_title="LookUp",
    page_icon="🔎",
    layout="wide"
)

st.image('img/2.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.sidebar.header("Pickup your news")
st.sidebar.caption('Media types')
agency_types = ['State', 'Independents', 'Foreign']
agency_selections = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign' else st.sidebar.toggle(agency) for agency in agency_types]
st.sidebar.caption('Categories')
categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
category_selections = [st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category) for category in categories]
# print(list(zip(categories, category_selections)))
st.sidebar.slider('News amount', 1, 10, 3)


st.write("# Search answers in the past")
st.info("Ask any question to our AI and get a strange magic")
st.divider()

text_input = st.text_input(
        "Enter your question here 👇",
        label_visibility="collapsed",
        disabled=False,
        placeholder="Enter your question here 👉")