import streamlit as st
from scripts.utils import get_df_from_handlers_response

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
# st.divider()

st.info("""
The antiSMI project explores and creates new ways of working with media for readers, journalists and researchers.\n
Here you can find a demonstration of what we came up with using Russian-language news as an example.
""")

# st.caption("<= Use the navigation bar on the left to easily navigate through these sections")


col1, col2 = st.columns(2)

with col1:
    st.write("""
    ## 🗞️ Now and Then:
    * The most popular news article of the day by categories
    * Picture of the day using the tag cloud
    * Ability to research all sources of any news on the agency's website
    * Day in the history
    * The most important news of the same day in the past

    ## 💨 Time Machine:
    * Most popular news article of any past period by categories in last 25 years
    * Picture of the selected period using the tag cloud
    * Ability to get direct agencies link to important news

    ## 🔎 LookUp:
    Ask any question about past events and get:
    * The answer our AI found appropriate
    * List of news articles with links that are similar to your query

    """)

with col2:
    st.write("""
    ## 📊 Visualizer:
    Here are graphs about the structure of Russian media and news flow:
    * What the Russian media will look like on the eve of 2022
    * AntiSMI structure
    * AntiSMI dynamics
    * etc

    ##  ⚗️ Fun Researching:
    This is where the fun research I discovered working on the project will be stored:
    * What aliens could understand by studying the Russian news
    * What are the Russian media?

    ## 📖 About:
    * Some info about projects
    * Technical information on how the project is made
    * Donate info if you want to support the project
    """)

# col1, col2 = st.columns(2)
#
# with col1:
#
#     st.page_link("pages/1_🗞️_Now_and_Then.py", label="Now and Then", icon="🗞️")
#     st.write("""
#     * The most popular news article of the day by categories
#     * Picture of the day using the tag cloud
#     * Ability to research all sources of any news on the agency's website
#     * Day in the history
#     * The most important news of the same day in the past
#     """)
#
#     st.page_link("pages/2_💨_Time_Machine.py", label="Time Machine", icon="💨️")
#     st.write("""
#     * Most popular news article of any past period by categories in last 25 years
#     * Picture of the selected period using the tag cloud
#     * Ability to get direct agencies link to important news
#     """)
#
#     st.page_link("pages/3_🔎_LookUp.py", label="LookUp", icon="🔎️")
#     st.write("""
#     Ask any question about past events and get:
#     * The answer our AI found appropriate
#     * List of news articles with links that are similar to your query
#     """)
#
#
# with col2:
#     st.page_link("pages/4_📊_Visualizer.py", label="Visualizer", icon="📊️")
#     st.write("""
#     Here are graphs about the structure of Russian media and news flow:
#     * What the Russian media will look like on the eve of 2022
#     * AntiSMI structure
#     * AntiSMI dynamics
#     * etc
#     """)
#
#     st.page_link("pages/5_⚗️_Fun_Researching.py", label="Fun Researching", icon="⚗️")
#     st.write("""
#     This is where the fun research I discovered working on the project will be stored:
#     * What aliens could understand by studying the Russian news
#     * What are the Russian media?
#     """)
#
#     st.page_link("pages/6_📖_About.py", label="About", icon="📖️")
#     st.write("""
#     * Some info about projects
#     * Technical information on how the project is made
#     * Donate info if you want to support the project
#     """)
