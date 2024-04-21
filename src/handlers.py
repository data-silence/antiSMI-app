"""
Uses handlers to retrieve news from the database and convert it into the required format
"""

import streamlit as st

import pandas as pd

import datetime as dt
from datetime import datetime
import requests
import json
from io import StringIO

from src.constants import api_url

"""Common"""


def get_response(handler: str) -> json:
    """Converts json received from asmi API-handlers to dataframe"""
    response = requests.get(handler)
    return response.json()


def get_df_from_response(handler: str) -> pd.DataFrame:
    response = get_response(handler)
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


"""For Asmi Service"""


@st.cache_data(show_spinner=False)
def get_today_news(user_date: dt.date, date_part: int, date_mode: str = 'all') -> pd.DataFrame:
    handler_url = f"/news/asmi/date_news/{user_date}/{date_part}/{date_mode}"
    handler = f"{api_url}{handler_url}"
    df_today_news = get_df_from_response(handler=handler)
    return df_today_news


@st.cache_data(show_spinner=False)
def get_all_agencies() -> pd.DataFrame:
    """Gets all agencies dataframe"""
    handler_url = "/agencies/all"
    handler = f"{api_url}{handler_url}"
    df_all_agencies = get_df_from_response(handler=handler)
    return df_all_agencies


"""For Timemachine Service"""


def get_url_from_tm(start_date: datetime.date, end_date: datetime.date, query: str = None) -> str:
    """Converts necessary link for requests to Timemachine Service"""
    if query is None:
        handler = f"{api_url}/news/tm/{start_date}/{end_date}"
    else:
        handler = f"{api_url}/news/tm/find_similar_news/{start_date}/{end_date}?query={query}"
    return handler


@st.cache_data(show_spinner=False)
def get_date_df_from_tm(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Get news data from Timemachine Service based on start date and end date"""
    handler = get_url_from_tm(start_date=start_date, end_date=end_date)
    date_df = get_df_from_response(handler=handler)
    return date_df


@st.cache_data(show_spinner=False)
def get_answer_df(start_date: datetime.date, end_date: datetime.date, query: str) -> pd.DataFrame:
    """Get news data from Timemachine Service based on user query and start date and end date"""
    handler = get_url_from_tm(start_date=start_date, end_date=end_date, query=query)
    answer_df = get_df_from_response(handler=handler)
    return answer_df


"""For Graphs"""


@st.cache_data(show_spinner=False)
def get_distinct_dates_news_df() -> pd.DataFrame:
    """Get dataframe of distinct news data from Timemachine Service for Visualizer"""
    handler = f"{api_url}/graphs/tm/distinct_dates"
    distinct_dates_news_df = get_df_from_response(handler=handler)
    return distinct_dates_news_df


@st.cache_data(show_spinner=False)
def get_digit_from_tm(value_name: str) -> str:
    """Allows you to fetch auxiliary values from the database for plotting purposes"""
    handler = f"{api_url}/graphs/tm/{value_name}"
    response = get_response(handler=handler)
    digit = json.dumps(response)
    return digit


# async def get_response(handler: str) -> json:
#     """Converts json received from asmi API-handlers to dataframe"""
#     async with httpx.AsyncClient() as client:
#         timeout = httpx.Timeout(10.0, read=None)
#         response = await client.get(handler, timeout=timeout)
#         return response.json()

if __name__ == "__main__":
    # emb = make_single_embs('Повышение цен на продукты')
    # print(emb)
    get_digit_from_tm('news_amount')
