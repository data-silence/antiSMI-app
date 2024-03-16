"""
Used to receive data from backend API and pre-process for further design of streamlit application
"""

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

import torch
from transformers import AutoTokenizer, AutoModel
from scripts.constants import tm_start_date, tm_last_date, api_url, default_categories

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("cointegrated/LaBSE-en-ru")
model = AutoModel.from_pretrained("cointegrated/LaBSE-en-ru").to(device)

"""
One-off scripts
"""


def select_random_date():
    delta = tm_last_date - tm_start_date
    return tm_start_date + dt.timedelta(random.randint(0, delta.days))


def make_single_embs(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, max_length=64, return_tensors='pt').to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
    embeddings = model_output.pooler_output
    embeddings = torch.nn.functional.normalize(embeddings)
    return embeddings[0].tolist()


def cos_simularity(a, b):
    cos_sim = np.dot(a, b) / (norm(a) * norm(b))
    return cos_sim


def find_sim_news(df: pd.DataFrame, q_emb: list[float]):
    df.loc[:, 'sim'] = df['embedding'].apply(lambda x: cos_simularity(q_emb, x))
    best_result = df[df.sim == df.sim.max()]
    return best_result


"""
From handlers interpreters
"""


@st.cache_data
def get_df_from_asmi(handler: str) -> pd.DataFrame:
    """Converts json received from asmi API-handlers to dataframe"""
    handler_url = f"{api_url}{handler}"
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


@st.cache_data
def get_date_df_from_tm(start_date: datetime.date, end_date: datetime.date) -> pd.DataFrame:
    """Converts json received from timemachine API-handlers to dataframe"""
    handler_url = f"{api_url}/news/tm/{str(start_date)}/{str(end_date)}"
    # print(handler_url)
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df


@st.cache_data
def get_answer(query: str) -> pd.DataFrame:
    """Sends sentence and get similar-news from API"""
    handler_url = f"{api_url}/news/tm/get_similar_news"
    embedding = make_single_embs(query)
    response = requests.post(handler_url, json=embedding).json()
    json_dump = json.dumps(response)
    similar_news_df = pd.read_json(StringIO(json_dump))
    similar_news_df.drop(columns='embedding', inplace=True)
    return similar_news_df


"""
Mixin to preprocess the dataframe into the Service format
"""


class DataframeMixin:
    @staticmethod
    def get_dataframe(df_type: str, media_type: str = None, start_date: datetime.date = None,
                      end_date: datetime.date = None) -> pd.DataFrame:
        df = None
        match df_type:
            case 'asmi_brief':
                df = get_df_from_asmi("/news/asmi/today/brief")
                df['embedding'] = df['news'].apply(lambda x: make_single_embs(x))
            case 'asmi_media_type':
                df = get_df_from_asmi(f"/news/asmi/today/{media_type}")
                df['embedding'] = df['news'].apply(lambda x: make_single_embs(x))
            case 'tm':
                df = get_date_df_from_tm(start_date=start_date, end_date=end_date)
        return df

    @staticmethod
    def get_clusters_columns(df_type: str, media_type: str = None, start_date: datetime.date = None,
                             end_date: datetime.date = None) -> pd.DataFrame:
        df = DataframeMixin.get_dataframe(df_type=df_type, media_type=media_type, start_date=start_date,
                                          end_date=end_date)

        if len(df) > 1:  # clustering is possible only if the number of news items is more than one
            model = AgglomerativeClustering(n_clusters=None, metric='cosine', linkage='complete',
                                            distance_threshold=0.3)
            labels = model.fit_predict(list(df.embedding))
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
    def filter_df(df: pd.DataFrame, amount: int, categories: list) -> pd.DataFrame:
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
class TimemachineService:
    """
    Class to handle news dataframes into news-digest for Timemachine service
    """
    service_name: str = 'tm'
    start_date: dt.date = None
    end_date: dt.date = start_date
    news_amount: int = 3
    categories: list[str] = field(default_factory=list)
    date_df: pd.DataFrame = None
    most_df: pd.DataFrame = None

    def __post_init__(self):
        self.categories = default_categories

    def set_params(self, start_date: dt.date, end_date: dt.date, news_amount: int, categories: list[str]):
        if self.date_df is None:
            self.date_df = DataframeMixin.get_clusters_columns(df_type=self.service_name, start_date=start_date,
                                                               end_date=end_date)
        compare_params = ((self.start_date, self.end_date, self.news_amount, self.categories) ==
                          (start_date, end_date, news_amount, categories))

        if not compare_params:
            if not (self.start_date, self.end_date) == (start_date, end_date):
                self.date_df = DataframeMixin.get_clusters_columns(df_type=self.service_name, start_date=start_date,
                                                                   end_date=end_date)
            self.most_df = DataframeMixin.filter_df(self.date_df, amount=news_amount, categories=categories)
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
            category_list = list(
                zip(category_df['date'], category_df['title'], category_df['resume'], category_df['links']))
            my_news.update({category: category_list})
        return my_news


@dataclass
class AsmiService:
    """
    Class to handle news dataframes into news-digest for AsmiService service
    """
    service_name: str = 'asmi_brief'
    media_type: str = None
    news_amount: int = 3
    categories: list[str] = field(default_factory=list)


    def __post_init__(self):
        # self.categories = default_categories
        self.date_df = DataframeMixin.get_clusters_columns(df_type=self.service_name, media_type=self.media_type)
        self.most_df = DataframeMixin.filter_df(self.date_df, amount=self.news_amount, categories=self.categories)

    def set_params(self, news_amount: int, categories: list[str]):
        self.most_df = DataframeMixin.filter_df(self.date_df, amount=news_amount, categories=categories)
        self.news_amount, self.categories = news_amount, categories

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
            category_list = list(
                zip(category_df['date'], category_df['title'], category_df['resume'], category_df['links']))
            my_news.update({category: category_list})
        return my_news


if __name__ == "__main__":
    emb = make_single_embs('Повышение цен на продукты')
    print(emb)
    # df = get_df_from_asmi("/news/asmi/today/brief")
    # print(df.head())
