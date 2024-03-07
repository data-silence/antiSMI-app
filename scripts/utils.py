import pandas as pd
import json
import requests
from io import StringIO
import streamlit as st

api_url = "http://127.0.0.1:8000"


# @st.cache_data
def get_df_from_asmi(handler: str) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}{handler}"
    # print(handler_url)
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


@st.cache_data
def get_df_from_handlers_response(handler: str) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}{handler}"
    # print(handler_url)
    response = requests.post(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


@st.cache_data
def digest_df() -> dict:
    result_df = get_df_from_handlers_response('/news/tm/get_date_news')
    my_news = {}
    for category in result_df.category.unique():
        category_df = result_df[result_df.category == category]
        # category_df.links = category_df.links.apply(lambda x: x.split())
        category_list = list(
            zip(category_df['date'], category_df['title'], category_df['resume'], category_df['links']))
        my_news.update({category: category_list})
    return my_news


if __name__ == "__main__":
    # df = get_df_from_handlers_response("last_quota")
    # print(df.head())
    test_url = f"{api_url}/api/generate"
    response = requests.post('{"model": "llama2", "prompt": "Why is the sky blue?"}')
