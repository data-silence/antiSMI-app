import datetime as dt

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

major_events = {
    1: {'start_date': dt.datetime(1999, 12, 31), 'end_date': dt.datetime(2000, 1, 3)},
    2: {'start_date': dt.datetime(2000, 3, 25), 'end_date': dt.datetime(2000, 3, 27)},
    3: {'start_date': dt.datetime(2000, 8, 12), 'end_date': dt.datetime(2000, 8, 15)},
    4: {'start_date': dt.datetime(2001, 9, 11), 'end_date': dt.datetime(2001, 9, 15)},
    5: {'start_date': dt.datetime(2002, 10, 23), 'end_date': dt.datetime(2002, 10, 26)},
    6: {'start_date': dt.datetime(2003, 10, 25), 'end_date': dt.datetime(2003, 10, 30)},
    7: {'start_date': dt.datetime(2004, 12, 25), 'end_date': dt.datetime(2004, 12, 27)},
    8: {'start_date': dt.datetime(2007, 12, 10), 'end_date': dt.datetime(2007, 12, 17)},
    9: {'start_date': dt.datetime(2008, 8, 7), 'end_date': dt.datetime(2008, 8, 12)},
    10: {'start_date': dt.datetime(2011, 9, 24), 'end_date': dt.datetime(2011, 9, 27)},
    11: {'start_date': dt.datetime(2011, 12, 4), 'end_date': dt.datetime(2011, 12, 6)},
    12: {'start_date': dt.datetime(2012, 5, 6), 'end_date': dt.datetime(2012, 5, 12)},
    13: {'start_date': dt.datetime(2014, 2, 22), 'end_date': dt.datetime(2014, 3, 1)},
}