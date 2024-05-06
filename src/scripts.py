"""
Used to receive data from backend API and pre-process for further design of streamlit application
"""

import pandas as pd
import numpy as np
from numpy.linalg import norm

import datetime as dt
from datetime import datetime
import pytz

import random

from src.constants import tm_start_date, tm_last_date

"""
One-off src
"""


def select_random_date() -> dt.date:
    """Selects a random date for the Time machine's random mode"""
    delta = tm_last_date - tm_start_date
    return tm_start_date + dt.timedelta(random.randint(0, delta.days))


def cosine_similarity(a, b) -> float:
    """Counts the cosine similarity between two vectors of embeddings of sentences"""
    cos_similarity = np.dot(a, b) / (norm(a) * norm(b))
    return cos_similarity


def find_sim_news(df: pd.DataFrame, q_emb: list[float]) -> pd.DataFrame:
    """Finds the best sentence based on cosine similarity"""
    df.loc[:, 'sim'] = df['embedding'].apply(lambda x: cosine_similarity(q_emb, x))
    best_result = df[df.sim == df.sim.max()]
    return best_result


def get_today_day_params() -> tuple[dt.date, int]:
    """Gets time part based on current Moscow time"""

    moscow_time = datetime.now(pytz.timezone('Europe/Moscow'))
    moscow_date = moscow_time.date()

    part = None

    if moscow_time.hour in range(0, 10):
        part = 0
    if moscow_time.hour in range(10, 14):
        part = 1
    if moscow_time.hour in range(14, 18):
        part = 2
    if moscow_time.hour in range(18, 22):
        part = 3
    if moscow_time.hour in range(22, 24):
        part = 4

    return moscow_date, part


def pymorphy2_311_hotfix():
    from inspect import getfullargspec
    from pymorphy2.units.base import BaseAnalyzerUnit

    def _get_param_names_311(klass):
        if klass.__init__ is object.__init__:
            return []
        args = getfullargspec(klass.__init__).args
        return sorted(args[1:])

    setattr(BaseAnalyzerUnit, '_get_param_names', _get_param_names_311)
