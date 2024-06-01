import streamlit as st

st.set_page_config(
    page_title="Power news",
    page_icon="🗞️",
    layout="wide"
)

st.sidebar.success("Select the section above")

st.image('img/1.png', use_column_width='auto',
         caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# Power news")

st.caption("Explore Russian life from the last 25 years to the present day through the news. We only give you the "
           "tools you need, the conclusions are always left to you")
st.info("""
Power news is a main part of an antiSMI Project that explores and creates new ways of working with media for readers, journalists and researchers.\n
Here you can find a demonstration of what we came up with using Russian-language news as an example. Other news languages cooming soon.
""")


col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ## 🗞️ Nowadays:
    * The most popular news article of today by categories
    * Ability to research all sources of any news on the agency's website
    * Picture of the day using the tag cloud
    * Ability to visually compare the day's news from different sources
    * A similar app for telegram: [Nowadays bot](https://t.me/antiSMI_bot)

    ## 📊 Visualizer:
    Here are graphs about the structure of Russian media and news flow:
    * What the Russian media will look like on the eve of 2022
    * AntiSMI structure and dynamics
    * Fun visualisations and research related to news studies

    ## 🔎 LookUp:
    Ask any question about past events and get:
    * The answer our AI found appropriate
    * A list of news articles with links similar to your query
    * A graph of changes in the number of news items related to your subject 
    """)

with col2:
    st.markdown("""
    ## 💨 Time Machine:
    The same capabilities as in the previous section, but with past news.
    There are 4 modes to explore past news with Time Machine:
    * Today in past: find out what happened on the same day many years ago
    * Presets: select any significant event in Russian history to discover the main news of that day
    * Manual: select the flight day to the past manually
    * Random: pick a random date in the past
    * A similar app for telegram: [Timemachine bot](https://t.me/time_mashine_bot) 

    ## 📖 About:
    * Information about antiSMI project
    * Technical details on how the project is made


    ## 🫰 Donate:
    * Donation information if you want to support the project
    """)


