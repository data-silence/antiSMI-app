"""
Used to receive data from backend API and pre-process for further design of streamlit application
"""

import pandas as pd
import streamlit as st
import datetime as dt
from datetime import datetime
import pytz

import json
from io import StringIO
from sklearn.cluster import AgglomerativeClustering
from dataclasses import dataclass, field
from collections import Counter
import numpy as np
from numpy.linalg import norm
import random
import requests

# import httpx
# import asyncio

from src.constants import tm_start_date, tm_last_date, api_url, categories_dict

# import torch
# from transformers import AutoTokenizer, AutoModel

#
# device = "cuda" if torch.cuda.is_available() else "cpu"
#
# tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")
# model = AutoModel.from_pretrained("cointegrated/LaBSE-en-ru").to(device)

"""
One-off src
"""


def select_random_date() -> dt.date:
    delta = tm_last_date - tm_start_date
    return tm_start_date + dt.timedelta(random.randint(0, delta.days))


# def make_single_embs(sentences):
#     encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt').to(device)
#     with torch.no_grad():
#         model_output = model(**encoded_input)
#     embeddings = model_output.pooler_output
#     embeddings = torch.nn.functional.normalize(embeddings)
#     return embeddings[0].tolist()


def cos_simularity(a, b):
    cos_sim = np.dot(a, b) / (norm(a) * norm(b))
    return cos_sim


def find_sim_news(df: pd.DataFrame, q_emb: list[float]):
    df.loc[:, 'sim'] = df['embedding'].apply(lambda x: cos_simularity(q_emb, x))
    best_result = df[df.sim == df.sim.max()]
    return best_result


def get_time_period(start_date: datetime.date = datetime.now(pytz.timezone('Europe/Moscow')),
                    end_date: datetime.date = None) -> tuple:
    if end_date is None:
        end_date = start_date

    start = datetime(year=start_date.year, month=start_date.month, day=start_date.day, hour=00, minute=00)
    end = datetime(year=end_date.year, month=end_date.month, day=end_date.day, hour=23, minute=59)
    one_day = dt.timedelta(days=1)
    part = None

    if start_date == datetime.today():
        if start_date.hour in range(0, 10):
            start = start.replace(hour=20, minute=56) - one_day
            end = end.replace(hour=22, minute=55) - one_day
            part = 0
        if start_date.hour in range(10, 14):
            start = start.replace(hour=22, minute=56) - one_day
            end = end.replace(hour=8, minute=55)
            part = 1
        if start_date.hour in range(14, 18):
            start = start.replace(hour=8, minute=56)
            end = end.replace(hour=12, minute=55)
            part = 2
        if start_date.hour in range(18, 22):
            start = start.replace(hour=12, minute=56)
            end = end.replace(hour=16, minute=55)
            part = 3
        if start_date.hour in range(22, 24):
            start = start.replace(hour=16, minute=56)
            end = end.replace(hour=20, minute=55)
            part = 4

    return start, end, part


"""
From handlers interpreters
"""

"""Common"""


# async def get_response(handler: str) -> json:
#     """Converts json received from asmi API-handlers to dataframe"""
#     async with httpx.AsyncClient() as client:
#         timeout = httpx.Timeout(10.0, read=None)
#         response = await client.get(handler, timeout=timeout)
#         return response.json()

def get_response(handler: str) -> json:
    """Converts json received from asmi API-handlers to dataframe"""
    response = requests.get(handler)
    return response.json()


def get_df_from_response(handler: str) -> pd.DataFrame:
    response = get_response(handler)
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


"""Get from Asmi Service"""


# @st.cache_data
def get_today_news_old_edition(start: dt.datetime, end: dt.datetime, part: str) -> pd.DataFrame:
    handler_url = "/news/asmi/today"
    handler = f"{api_url}{handler_url}"
    df_today_news = get_df_from_response(handler=handler)
    st.caption(
        f"This is today the part #{part} news digest. The last packet has been received for period between "
        f"{start} and {end}")
    return df_today_news


@st.cache_data
def get_today_news(user_date: dt.date) -> pd.DataFrame:
    handler_url = f"/news/asmi/date_news/{user_date}"
    handler = f"{api_url}{handler_url}"
    df_today_news = get_df_from_response(handler=handler)
    return df_today_news


@st.cache_data
def get_all_agencies():
    handler_url = "/agencies/all"
    handler = f"{api_url}{handler_url}"
    df_all_agencies = get_df_from_response(handler=handler)
    return df_all_agencies


"""Get from Timemachine Service"""


def get_url_from_tm(start_date: datetime.date, end_date: datetime.date, query: str = None) -> str:
    """Converts json received from timemachine API-handlers to dataframe"""
    if query is None:
        handler = f"{api_url}/news/tm/{start_date}/{end_date}"
    else:
        handler = f"{api_url}/news/tm/find_similar_news/{start_date}/{end_date}?query={query}"
    return handler


@st.cache_data
def get_date_df_from_tm(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    handler = get_url_from_tm(start_date=start_date, end_date=end_date)
    date_df = get_df_from_response(handler=handler)
    return date_df


@st.cache_data(show_spinner=False)
def get_answer_df(start_date: datetime.date, end_date: datetime.date, query: str) -> pd.DataFrame:
    handler = get_url_from_tm(start_date=start_date, end_date=end_date, query=query)
    answer_df = get_df_from_response(handler=handler)
    return answer_df


"""Get for Graphs"""


@st.cache_data
def get_distinct_dates_news_df() -> pd.DataFrame:
    """Converts json received from timemachine API-handlers to dataframe"""
    handler = f"{api_url}/graphs/tm/distinct_dates"
    distinct_dates_news_df = get_df_from_response(handler=handler)
    return distinct_dates_news_df


# @st.cache_data
# def get_digit_from_tm(value_name: str):
#     """Get some digits from timemachine API-handlers"""
#     handler = f"{api_url}/graphs/tm/{value_name}"
#     response = asyncio.run(get_response(handler=handler))
#     digit = json.dumps(response)
#     return digit


@st.cache_data
def get_digit_from_tm(value_name: str):
    """Get some digits from timemachine API-handlers"""
    handler = f"{api_url}/graphs/tm/{value_name}"
    response = get_response(handler=handler)
    digit = json.dumps(response)
    return digit


"""
Mixin to preprocess the dataframe into the Service format
"""


class DataframeMixin:

    @staticmethod
    # @st.cache_data(show_spinner=False)
    def get_dataframe(service_name: str, start_date: datetime.date = None,
                      end_date: datetime.date = None) -> pd.DataFrame:
        df = None

        match service_name:
            case 'asmi':
                user_date = datetime.now(pytz.timezone('Europe/Moscow')).date()
                df = get_today_news(user_date=user_date)
            case 'tm':
                df = get_date_df_from_tm(start_date=start_date, end_date=end_date)
        return df

    @staticmethod
    def get_clusters_columns(service_name: str, start_date: datetime.date = None,
                             end_date: datetime.date = None) -> pd.DataFrame:
        df = DataframeMixin.get_dataframe(service_name=service_name, start_date=start_date,
                                          end_date=end_date)

        if len(df) > 1:  # clustering is possible only if the number of news items is more than one
            clust_model = AgglomerativeClustering(n_clusters=None, metric='cosine', linkage='complete',
                                                  distance_threshold=0.3)
            labels = clust_model.fit_predict(list(df.embedding))
            df.loc[:, 'label'] = labels

        elif len(df) == 1:  # if there is only one news item, we assign it a label = -1
            df.loc[:, 'label'] = -1
        # To avoid putting the same news in different categories, we assign the most frequent category to one label
        trans = df.groupby(by=['label'])['category'].agg(pd.Series.mode)
        df['new'] = df.label.apply(lambda x: trans.iloc[x])
        # Leave only one value if the mod produces multiple values in np.ndarray
        df.loc[:, 'new'] = df.new.apply(lambda x: x[0] if isinstance(x, np.ndarray) else x)

        # Removing auxiliary columns and sorting
        df.drop(columns='category', inplace=True)
        df.rename(columns={'new': 'category'}, inplace=True)
        df.sort_values(by=['category', 'label'], ascending=True, inplace=True)
        return df

    @staticmethod
    def filter_df(df: pd.DataFrame, amount: int, categories: list, media_type: list) -> pd.DataFrame:
        if media_type:
            df = df.loc[df['category'].isin(categories) & df['media_type'].isin(media_type)]
        else:
            df = df.loc[df['category'].isin(categories)]

        final_labels = []
        for category in categories:
            most_tuple = Counter(list(df.label[df.category == category])).most_common(amount)
            most_labels = [el[0] for el in most_tuple]
            final_labels.extend(most_labels)
        return df[df.label.isin(final_labels)]


"""
News Services 
"""


@dataclass
class Service:
    news_amount: int = 3
    categories: list[str] = field(default_factory=list)
    date_df: pd.DataFrame = None
    most_df: pd.DataFrame = None

    def get_source_links(self, title: str):
        cluster = self.most_df.label[self.most_df.title == title].iloc[0]

        links_set = set()
        links = self.most_df['links'][self.most_df.label == cluster].tolist()
        urls = self.most_df['url'][self.most_df.label == cluster].tolist()
        for group in links:
            group = group.split(',')
            links_set.update(group)
        links_set.update(urls)
        return ' '.join(list(links_set))

    def leave_me_alone(self) -> pd.DataFrame:
        unique_labels = set(self.most_df.label.tolist())
        url_final_list = []
        for label in unique_labels:
            avg_emb = np.array(list(self.most_df.embedding[self.most_df.label == label])).mean(axis=0)
            best_url = find_sim_news(self.most_df, avg_emb).url.index[0]
            url_final_list.append(best_url)
        final_df = self.most_df[self.most_df.index.isin(url_final_list)].drop(columns=['sim', 'embedding', 'label'])
        final_df.links = final_df.title.apply(lambda x: self.get_source_links(x))
        return final_df

    def digest_dict(self) -> dict:
        result_df = self.leave_me_alone()
        my_news = {}
        for category in result_df.category.unique():
            category_df = result_df[result_df.category == category]
            category_list = list(
                zip(category_df['date'], category_df['title'], category_df['resume'], category_df['links']))
            my_news.update({category: category_list})
        return my_news


@dataclass
class AsmiService(Service):
    """
    Class to handle news dataframes into news-digest for AsmiService service
    """
    service_name: str = 'asmi'
    media_type: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.categories = [category for category in categories_dict]
        self.date_df = DataframeMixin.get_clusters_columns(service_name=self.service_name)
        self.most_df = DataframeMixin.filter_df(self.date_df, amount=self.news_amount, categories=self.categories,
                                                media_type=self.media_type)

    def set_params(self, news_amount: int, categories: list[str], media_type: list):
        self.most_df = DataframeMixin.filter_df(self.date_df, amount=news_amount, categories=categories,
                                                media_type=media_type)
        self.news_amount, self.categories, self.media_type = news_amount, categories, media_type


@dataclass
class TimemachineService(Service):
    """
    Class to handle news dataframes into news-digest for Timemachine service
    """
    service_name: str = 'tm'
    start_date: dt.date = None
    end_date: dt.date = start_date
    media_type: list = None

    def __post_init__(self):
        self.categories = categories_dict.keys()

    def set_params(self, start_date: dt.date, end_date: dt.date, news_amount: int, categories: list[str]):
        if self.date_df is None:
            self.date_df = DataframeMixin.get_clusters_columns(service_name=self.service_name, start_date=start_date,
                                                               end_date=end_date)
        compare_params = ((self.start_date, self.end_date, self.news_amount, self.categories) ==
                          (start_date, end_date, news_amount, categories))

        if not compare_params:
            if not (self.start_date, self.end_date) == (start_date, end_date):
                self.date_df = DataframeMixin.get_clusters_columns(service_name=self.service_name,
                                                                   start_date=start_date,
                                                                   end_date=end_date)
            self.most_df = DataframeMixin.filter_df(self.date_df, amount=news_amount, categories=categories,
                                                    media_type=self.media_type)
        self.start_date, self.end_date, self.news_amount, self.categories = (
            start_date, end_date, news_amount, categories)


if __name__ == "__main__":
    # emb = make_single_embs('Повышение цен на продукты')
    # print(emb)
    get_digit_from_tm('news_amount')
