import pandas as pd
import streamlit as st
import datetime as dt
from datetime import datetime

import json
import requests
from io import StringIO
from sklearn.cluster import AgglomerativeClustering
from dataclasses import dataclass, field
from collections import Counter
import numpy as np
from numpy.linalg import norm
import random

api_url = "http://127.0.0.1:8000"
default_categories = ['economy', 'technology', 'entertainment', 'science', 'sports']
categories_dict = {
    'economy': {'emoj': '💰'},
    'science': {'emoj': '🔬'},
    'sports': {'emoj': '🏃'},
    'technology': {'emoj': '📲'},
    'entertainment': {'emoj': '👻'},
    'society': {'emoj': '👲'}
}

tm_start_date = dt.date(1999, 8, 31)
tm_last_date = dt.date(2023, 12, 31)


def select_random_date():
    delta = tm_last_date - tm_start_date
    return tm_start_date + dt.timedelta(random.randint(0, delta.days))


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
def get_date_df_from_tm(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}/news/tm/{str(start_date)}/{str(end_date)}"
    print(handler_url)
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


def get_clusters_columns(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    df = get_date_df_from_tm(start_date=start_date, end_date=end_date)

    if len(df) > 1:  # кластеризацию возможно сделать только если количество новостей более одной
        model = AgglomerativeClustering(n_clusters=None, metric='cosine', linkage='complete',
                                        distance_threshold=0.3)
        labels = model.fit_predict(list(df.embedding))
        df.loc[:, 'label'] = labels

    elif len(df) == 1:  # если новость одна - присваиваем ей лейбл = -1
        df.loc[:, 'label'] = -1
    # чтобы избежать отнесения одной новости по разным категориям, присвоим одному лейблу наиболее частую категорию,
    trans = df.groupby(by=['label'])['category'].agg(pd.Series.mode)
    df['new'] = df.label.apply(lambda x: trans.iloc[x])
    # Оставляем только одно значение, если мода выдаёт несколько значений в np.ndarray
    df.loc[:, 'new'] = df.new.apply(lambda x: x[0] if isinstance(x, np.ndarray) else x)

    # Удаляем вспомогательные столбцы и сортируем
    df.drop(columns='category', inplace=True)
    df.rename(columns={'new': 'category'}, inplace=True)
    df.sort_values(by=['category', 'label'], ascending=True, inplace=True)

    return df


@st.cache_data
def filter_df(df: pd.DataFrame, amount: int, categories: list) -> pd.DataFrame:
    df = df.loc[df['category'].isin(categories)]
    final_labels = []
    for category in categories:
        most_tuple = Counter(list(df.label[df.category == category])).most_common(amount)
        most_labels = [el[0] for el in most_tuple]
        final_labels.extend(most_labels)
    return df[df.label.isin(final_labels)]


def cos_simularity(a, b):
    cos_sim = np.dot(a, b) / (norm(a) * norm(b))
    return cos_sim


def find_sim_news(df: pd.DataFrame, q_emb: list[float]):
    df.loc[:, 'sim'] = df['embedding'].apply(lambda x: cos_simularity(q_emb, x))
    best_result = df[df.sim == df.sim.max()]
    return best_result


@dataclass
class NewsService:
    service_name: str = 'asmi'
    start_date: dt.date = dt.date.today()
    end_date: dt.date = start_date
    news_amount: int = 3
    categories: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.categories = default_categories
        self.date_df = get_clusters_columns(start_date=self.start_date, end_date=self.end_date)
        self.most_df = filter_df(self.date_df, amount=self.news_amount, categories=self.categories)

    def set_params(self, start_date: dt.date, end_date: dt.date, news_amount: int, categories: list[str]):
        compare_params = (
                self.start_date, self.end_date, self.news_amount, self.categories ==
                start_date, end_date, news_amount, categories
        )
        if not compare_params:
            self.most_df = filter_df(self.date_df, amount=self.news_amount, categories=self.categories)
            if not (self.start_date, self.end_date) == (start_date, end_date):
                self.date_df = get_clusters_columns(start_date=start_date, end_date=end_date)
        self.start_date, self.end_date, self.news_amount, self.categories = start_date, end_date, news_amount, categories

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

    def digest_df(self) -> dict:
        result_df = self.leave_me_alone()
        my_news = {}
        for category in result_df.category.unique():
            category_df = result_df[result_df.category == category]
            # category_df.links = category_df.links.apply(lambda x: x.split())
            category_list = list(
                zip(category_df['date'], category_df['title'], category_df['resume'], category_df['links']))
            my_news.update({category: category_list})
        return my_news


# @st.cache_data
# def get_df_from_handlers_response(handler: str) -> pd.DataFrame:
#     """Converts json received from API to dataframe"""
#     handler_url = f"{api_url}{handler}"
#     response = requests.post(handler_url).json()
#     json_dump = json.dumps(response)
#     df = pd.read_json(StringIO(json_dump))
#     return df


if __name__ == "__main__":
    # df = get_df_from_handlers_response("last_quota")
    # print(df.head())
    test_url = f"{api_url}/api/generate"
    response = requests.post('{"model": "llama2", "prompt": "Why is the sky blue?"}')
