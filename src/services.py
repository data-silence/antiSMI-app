"""
Mixins and Classes used for processing and storing news
"""

import datetime as dt
from datetime import datetime

from dataclasses import dataclass, field
from collections import Counter

import pandas as pd
import numpy as np

from sklearn.cluster import AgglomerativeClustering

from src.constants import categories_dict
from src.handlers import get_today_news, get_date_df_from_tm
from src.scripts import get_today_day_params, find_sim_news

"""
Mixin to preprocess the dataframe into the Service format
"""


class DataframeMixin:
    """Functions common to News Services for processing news dataframes are stored here"""

    @staticmethod
    # @st.cache_data(show_spinner=False)
    def get_dataframe(service_name: str, start_date: datetime.date = None,
                      end_date: datetime.date = None, date_mode: str = None) -> pd.DataFrame:
        """Gets the news dataframe based on the service name, start date and end date"""
        df = None

        match service_name:
            case 'asmi':
                user_date, part = get_today_day_params()
                df = get_today_news(user_date=user_date, date_part=part, date_mode=date_mode)
            case 'tm':
                df = get_date_df_from_tm(start_date=start_date, end_date=end_date)
        return df

    @staticmethod
    def get_clusters_columns(service_name: str, start_date: datetime.date = None,
                             end_date: datetime.date = None, date_mode: str = None) -> pd.DataFrame:
        """Assigns a label to each news item based on the agglomerate clustering performed"""
        df = DataframeMixin.get_dataframe(service_name=service_name, start_date=start_date,
                                          end_date=end_date, date_mode=date_mode)

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
        """The received news dataframe is filtered based on the filters applied by the user"""
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


@dataclass
class Service:
    """Used to initialise news services and define methods common to all types of services"""
    news_amount: int = 3
    categories: list[str] = field(default_factory=list)
    date_df: pd.DataFrame = None
    most_df: pd.DataFrame = None

    def get_source_links(self, title: str) -> str:
        """Collects links to primary sources to form news digests"""
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
        """Forms the final representation of the news dataframe, removes unnecessary columns"""
        unique_labels = set(self.most_df.label.tolist())
        url_final_list = []
        for label in unique_labels:
            avg_emb = np.array(list(self.most_df.embedding[self.most_df.label == label])).mean(axis=0)
            best_url = find_sim_news(self.most_df, avg_emb).url.index[0]
            url_final_list.append(best_url)
        final_df = self.most_df[self.most_df.index.isin(url_final_list)].drop(columns=['embedding', 'label'])
        final_df.links = final_df.title.apply(lambda x: self.get_source_links(x))
        return final_df

    def digest_dict(self) -> dict:
        """Converts the news dataframe into a news dictionary for digest processing"""
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
    date_mode: str = 'all'

    def __post_init__(self):
        """Initialise the news dataframes as class attributes"""
        self.categories = [category for category in categories_dict]
        self.date_df = DataframeMixin.get_clusters_columns(service_name=self.service_name, date_mode=self.date_mode)
        self.most_df = DataframeMixin.filter_df(self.date_df, amount=self.news_amount, categories=self.categories,
                                                media_type=self.media_type)

    def set_params(self, news_amount: int, categories: list[str], media_type: list):
        """Sets parameters for digest processing depending on users choice"""
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
        """Sets parameters for digest processing depending on users choice"""
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
