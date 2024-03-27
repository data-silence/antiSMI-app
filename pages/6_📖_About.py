import streamlit as st

st.set_page_config(
    page_title="AntiSMI project",
    page_icon="📰️",
    layout="wide"
)

st.image('img/6.png', use_column_width='auto',
             caption='Developing tools for media and social researchers: enjoy-ds@pm.me')

st.write("# About project")
st.divider()
st.sidebar.header("About")

st.markdown(
    """
This site is only part of the project, and serves as a testing demonstration of newsroom ideas.
AntiSMI project is a research and still non-profit project at the intersection of ML and journalism that uses 
machine learning models to analyse changes in the news flow in real time, trying to create a fundamentally 
different way of consuming news in modern society.

The project started with collecting and analysing information about partners of Yandex-news service as of the 
beginning of last peaceful summer 2021. 

Due to stupid events around here, it keeps growing and changing and I have no control over it anymore. I don't know 
when or how it will end.

If you have any questions, ideas or you would like to collaborate, do not hesitate to contact me:   
    """
)
st.divider()
st.markdown(
    """
### Key features:
**Project start date:** 2022-07-01

**GitHub:**  1

**Performance:** ~50 news agencies, ~1 000 news/day

**Volume of available base:** ~2 million news articles [08.1999 - today]
    """
)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    ### ⚓ Pipeline

    - **Scraping**
        - requests
        - beatufill soup 4
    - **Summarisation**
        - mBart, Seq2Seq, pretrained [news summary]
        - ruT5, pretrained [title]
    - **Categorization**
        - fasttext, supervised on 7 classes
    - **Clustering**
        - glove-embeddings Navec (trained on the news corps)
        - sklearn: agglomerative clustering by cosine distance with a tuned threshold
    - **Interaction interfaces**
        - this web app
        - telegram bots
        - SuperSet [analytics, dashboards]
        """
    )



with col2:
    st.markdown(
        """
    ### ⚙️ Stack

    - **Languages:** Python, SQL and SQLalchemy

    - **Backend:** FastAPI

    - **Frontend:** Streamlit, aiogram and pyTelegramBot

    - **Data Bases:** PostgreSQL

    - **Data validation:** Pydantic

    - **Logging:** Loguru

    - **BI**: Apache SuperSet
        """
    )
    st.divider()
    st.markdown(
        """
    ### 🔨 Development tools
    
    - Pycharm
    - Docker
    - GitHub
    - Linux shell
        """
    )