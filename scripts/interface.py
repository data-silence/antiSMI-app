import streamlit as st


def draw_sidebar():
    st.sidebar.header("Pickup news you want:")
    news_amount_selection = st.sidebar.slider('News amount', 1, 10, 3)
    st.sidebar.caption('Media types')
    agency_types = ['State', 'Independents', 'Foreign']
    agency_selection = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign' else st.sidebar.toggle(agency) for
                        agency in agency_types]
    st.sidebar.caption('Categories')
    categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
    category_selection = [
        st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category)
        for category in categories]
    if category_selection[3]:
        st.toast('Выбор этой категории не доступен бесплатным пользователям.')
    return news_amount_selection, category_selection, agency_selection
