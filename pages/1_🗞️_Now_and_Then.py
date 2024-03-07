import streamlit as st
from scripts.utils import digest_df

st.set_page_config(
    page_title="Nowdays",
    page_icon="🗞️",
    layout="wide"
)

categories_dict = {
    'economy': {'emoj': '💰'},
    'science': {'emoj': '🔬'},
    'sports': {'emoj': '🏃'},
    'technology': {'emoj': '📲'},
    'entertainment': {'emoj': '👻'},
    'society': {'emoj': '👲'}
}

st.image('img/6.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Russian news for 25 years till nowadays")
st.info("What is happening in Russia today? What happened on the same day in the past?")
# st.divider()

st.sidebar.header("Pickup news you want:")
st.sidebar.slider('News amount', 1, 10, 3)
st.sidebar.caption('Media types')
agency_types = ['State', 'Independents', 'Foreign']
agency_selections = [st.sidebar.toggle(agency, value=True) if agency != 'Foreign' else st.sidebar.toggle(agency) for
                     agency in agency_types]
st.sidebar.caption('Categories')
categories = ['Economy', 'Science', 'Technology', 'Society', 'Entertainment', 'Sports']  # Change to sql-query
category_selections = [st.sidebar.toggle(category, value=True) if category != 'Society' else st.sidebar.toggle(category)
                       for category in categories]
# print(list(zip(categories, category_selections)))


# df = get_df_from_handlers_response('/news/tm/get_date_news')
# st.dataframe(df, use_container_width=True)

my_news = digest_df()

selected_categories = list(my_news.keys())
columns = st.columns(len(my_news))
for i, column in enumerate(columns):
    category = selected_categories[i]
    emoj = categories_dict[category]['emoj']
    all_news = my_news[category]
    column.subheader(emoj + ' ' + category.title())
    for news in all_news:
        column.caption(news[0].time().isoformat(timespec='minutes'))
        column.write(news[1])
        capt = column.expander("...", False)
        capt.caption('News resume:')
        capt.caption(news[2])
        links_list = news[3].split(',')
        sourse = [f"<a href='{el}'>{i + 1}</a>" for i, el in enumerate(links_list)]
        capt.caption(f'sources & related: {sourse}', unsafe_allow_html=True)
