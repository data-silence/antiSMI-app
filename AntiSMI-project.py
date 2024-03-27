import streamlit as st

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="🗞️",
    layout="wide"
)

st.sidebar.success("Select the section above")

st.image('img/1.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# AntiSMI project")
st.caption("Explore Russian life from the last 25 years to the present day through the news. We only give you the "
           "tools you need, the conclusions are always left to you")

st.info("""
The antiSMI project explores and creates new ways of working with media for readers, journalists and researchers.\n
Here you can find a demonstration of what we came up with using Russian-language news as an example.
""")

col1, col2 = st.columns(2)

with col1:
    st.write("""
    ## 🗞️ Nowadays:
    * The most popular news article of today by categories
    * Ability to research all sources of any news on the agency's website
    * Picture of the day using the tag cloud

    ## 📊 Visualizer:
    Here are graphs about the structure of Russian media and news flow:
    * What the Russian media will look like on the eve of 2022
    * AntiSMI structure and dynamics
    * Fun visualisations and research related to news studies

    ## 🔎 LookUp:
    Ask any question about past events and get:
    * The answer our AI found appropriate
    * List of news articles with links that are similar to your query
    * Graph of changes in the number of news items of the required subject 
    """)

with col2:
    st.write("""
    ## 💨 Time Machine:
    The same ability as in the previous section, but with the past news. There are 4 modes to exploring past news with Time Machine:
    * Today in past: find out what happened on the same day many years ago
    * Presets: select any specified important event in the history of Russia to find out the main news of that day
    * Manual: select the flight day to the past manually
    * Random: let you to pick a date in the past automatically 

    ## 📖 About:
    * Some info about projects
    * Technical information on how the project is made


    ## 🫰 Donate:
    * Donate info if you want to support the project
    """)
