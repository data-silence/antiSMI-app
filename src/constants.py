"""Stores immutable data - common constants, dictionaries, lists"""

import datetime as dt
# import os
# from dotenv import load_dotenv

import nltk
from nltk.corpus import stopwords

nltk.download("stopwords", quiet=True)

# api_url = "http://127.0.0.1:8000"
# load_dotenv()
# api_url = os.getenv("API_URL")

api_url = "http://backend:8000"

categories_dict = {
    'economy': {'emoj': '💰'},
    'science': {'emoj': '🔬'},
    'sports': {'emoj': '🏃'},
    'technology': {'emoj': '📲'},
    'entertainment': {'emoj': '👻'},
    'society': {'emoj': '👲'}
}

media_types_dict = {'state': '💀️', 'independents': '🐈', 'foreign': '👽'}

translation_countries = {'russian': 'Россия', 'ukranian': 'Украина', 'non ukranian': 'неУкраина'}

tm_start_date = dt.date(1999, 8, 31)
tm_last_date = dt.date(2021, 12, 31)

major_events = (
    {'start_date': dt.datetime(1999, 12, 31), 'end_date': dt.datetime(2000, 1, 3),
     'description': "Yeltsin's resignation"},
    {'start_date': dt.datetime(2000, 3, 25), 'end_date': dt.datetime(2000, 3, 27), 'description': "President Putin"},
    {'start_date': dt.datetime(2000, 8, 12), 'end_date': dt.datetime(2000, 8, 15), 'description': "Kursk"},
    {'start_date': dt.datetime(2001, 9, 11), 'end_date': dt.datetime(2001, 9, 15), 'description': "September 11"},
    {'start_date': dt.datetime(2002, 10, 23), 'end_date': dt.datetime(2002, 10, 26), 'description': "Nord-Ost"},
    {'start_date': dt.datetime(2003, 10, 25), 'end_date': dt.datetime(2003, 10, 30), 'description': "Yukos case"},
    {'start_date': dt.datetime(2003, 11, 2), 'end_date': dt.datetime(2003, 11, 4), 'description': "Rose Revolution"},
    {'start_date': dt.datetime(2004, 2, 24), 'end_date': dt.datetime(2004, 2, 24),
     'description': "Kasyanov's resignation"},
    {'start_date': dt.datetime(2004, 3, 14), 'end_date': dt.datetime(2004, 3, 14),
     'description': "Putin's second term"},
    {'start_date': dt.datetime(2004, 3, 29), 'end_date': dt.datetime(2004, 3, 29),
     'description': "Nato expansion"},
    {'start_date': dt.datetime(2004, 5, 9), 'end_date': dt.datetime(2004, 5, 9),
     'description': "Death of Akhmat Kadyrov"},
    {'start_date': dt.datetime(2004, 6, 1), 'end_date': dt.datetime(2004, 6, 1),
     'description': "Parfenov's resignation"},
    {'start_date': dt.datetime(2004, 9, 1), 'end_date': dt.datetime(2004, 9, 3),
     'description': "Beslan"},
    {'start_date': dt.datetime(2004, 12, 19), 'end_date': dt.datetime(2004, 12, 19),
     'description': "Baikalfinancegroup"},
    {'start_date': dt.datetime(2004, 12, 25), 'end_date': dt.datetime(2004, 12, 27),
     'description': "Orange Revolution"},
    {'start_date': dt.datetime(2005, 3, 20), 'end_date': dt.datetime(2005, 3, 25),
     'description': "Tulip Revolution"},
    {'start_date': dt.datetime(2005, 5, 31), 'end_date': dt.datetime(2005, 5, 31),
     'description': "Khodorkovsky verdict"},
    {'start_date': dt.datetime(2006, 6, 3), 'end_date': dt.datetime(2006, 6, 3),
     'description': "Independence of Montenegro and Serbia"},
    {'start_date': dt.datetime(2007, 12, 10), 'end_date': dt.datetime(2007, 12, 17),
     'description': "Medvedev as Preemnik"},
    {'start_date': dt.datetime(2008, 8, 7), 'end_date': dt.datetime(2008, 8, 12), 'description': "Georgian war"},
    {'start_date': dt.datetime(2009, 1, 20), 'end_date': dt.datetime(2009, 1, 20), 'description': "President Obama"},
    {'start_date': dt.datetime(2009, 11, 16), 'end_date': dt.datetime(2009, 11, 16), 'description': "Magnitskiy death"},
    {'start_date': dt.datetime(2010, 1, 19), 'end_date': dt.datetime(2010, 1, 19), 'description': "SKFO"},
    {'start_date': dt.datetime(2010, 9, 28), 'end_date': dt.datetime(2010, 9, 28),
     'description': "Luzhkov's resignation"},
    {'start_date': dt.datetime(2010, 10, 21), 'end_date': dt.datetime(2010, 10, 21),
     'description': "Mayor Sobyanin"},
    {'start_date': dt.datetime(2010, 12, 16), 'end_date': dt.datetime(2010, 12, 16),
     'description': "Magnitsky Act"},
    {'start_date': dt.datetime(2011, 9, 24), 'end_date': dt.datetime(2011, 9, 27), 'description': "Putin's back"},
    {'start_date': dt.datetime(2011, 12, 4), 'end_date': dt.datetime(2011, 12, 6), 'description': "Bolotnaya rallies"},
    {'start_date': dt.datetime(2012, 5, 6), 'end_date': dt.datetime(2012, 5, 12), 'description': "Million Man March"},
    {'start_date': dt.datetime(2014, 2, 22), 'end_date': dt.datetime(2014, 3, 1),
     'description': "Annexation of Crimea"},
    {'start_date': dt.datetime(2014, 7, 17), 'end_date': dt.datetime(2014, 7, 17),
     'description': "Boeing 777 MH17 crash"},
    {'start_date': dt.datetime(2014, 9, 5), 'end_date': dt.datetime(2014, 9, 5), 'description': "Minsk I agreements"},
    {'start_date': dt.datetime(2015, 2, 11), 'end_date': dt.datetime(2015, 2, 12),
     'description': "Minsk II agreements"},
    {'start_date': dt.datetime(2015, 11, 24), 'end_date': dt.datetime(2015, 11, 24),
     'description': "Sukhoi Su-24 shootdown"},
    {'start_date': dt.datetime(2015, 12, 15), 'end_date': dt.datetime(2015, 12, 15), 'description': "MIR Card Payment"},
    {'start_date': dt.datetime(2016, 4, 2), 'end_date': dt.datetime(2016, 4, 2),
     'description': "Nagorno-Karabakh conflict"},
    {'start_date': dt.datetime(2016, 7, 15), 'end_date': dt.datetime(2016, 7, 16),
     'description': "Turkish coup attempt"},
    {'start_date': dt.datetime(2016, 7, 28), 'end_date': dt.datetime(2016, 7, 28),
     'description': "Crimea as a Russian South District"},
    {'start_date': dt.datetime(2016, 11, 8), 'end_date': dt.datetime(2016, 11, 8),
     'description': "Trump won the election"},
    {'start_date': dt.datetime(2016, 12, 25), 'end_date': dt.datetime(2016, 12, 25),
     'description': "Defence Ministry Tu-154 crash"},
    {'start_date': dt.datetime(2017, 5, 14), 'end_date': dt.datetime(2017, 5, 14), 'description': "President Macron"},
    {'start_date': dt.datetime(2018, 3, 16), 'end_date': dt.datetime(2018, 3, 20),
     'description': "Russian presidential election"},
    {'start_date': dt.datetime(2018, 3, 25), 'end_date': dt.datetime(2018, 3, 25), 'description': "Kemerovo fire"},
    {'start_date': dt.datetime(2018, 4, 23), 'end_date': dt.datetime(2018, 4, 30),
     'description': "Armenian Revolution"},
    {'start_date': dt.datetime(2018, 5, 16), 'end_date': dt.datetime(2018, 5, 16), 'description': "Crimean Bridge"},
    {'start_date': dt.datetime(2018, 11, 25), 'end_date': dt.datetime(2018, 11, 25),
     'description': "Kerch Strait incident"},
    {'start_date': dt.datetime(2018, 12, 15), 'end_date': dt.datetime(2018, 12, 15),
     'description': "Moscow–Constantinople schism"},
    {'start_date': dt.datetime(2019, 3, 19), 'end_date': dt.datetime(2019, 3, 19),
     'description': "Nazarbaev's resignation"},
    {'start_date': dt.datetime(2019, 4, 15), 'end_date': dt.datetime(2019, 4, 15), 'description': "Notre-Dame fire"},
    {'start_date': dt.datetime(2019, 4, 21), 'end_date': dt.datetime(2019, 4, 22), 'description': "President Zelensky"},
    {'start_date': dt.datetime(2019, 5, 1), 'end_date': dt.datetime(2019, 5, 1),
     'description': "Sovereign Internet Law"},
    {'start_date': dt.datetime(2019, 7, 24), 'end_date': dt.datetime(2019, 7, 24),
     'description': "Prime Minister Boris Johnson"},
    {'start_date': dt.datetime(2019, 11, 11), 'end_date': dt.datetime(2019, 11, 11),
     'description': "Hong Kong protests starts"},
    {'start_date': dt.datetime(2019, 11, 19), 'end_date': dt.datetime(2019, 11, 21),
     'description': "Foreign agent law"},
    {'start_date': dt.datetime(2019, 12, 8), 'end_date': dt.datetime(2019, 12, 8), 'description': "Covid starts"},
    {'start_date': dt.datetime(2020, 1, 15), 'end_date': dt.datetime(2020, 1, 16), 'description': "New cabinet"},
    {'start_date': dt.datetime(2020, 1, 24), 'end_date': dt.datetime(2020, 1, 31), 'description': "Brexit"},
    {'start_date': dt.datetime(2020, 3, 11), 'end_date': dt.datetime(2020, 3, 11), 'description': "Pandemia starts"},
    {'start_date': dt.datetime(2020, 5, 25), 'end_date': dt.datetime(2020, 5, 27),
     'description': "Murder of George Floyd"},
    {'start_date': dt.datetime(2020, 6, 25), 'end_date': dt.datetime(2020, 7, 1),
     'description': "Сonstitutional referendum"},
    {'start_date': dt.datetime(2020, 7, 9), 'end_date': dt.datetime(2020, 7, 9), 'description': "Furgal's arrest"},
    {'start_date': dt.datetime(2020, 8, 9), 'end_date': dt.datetime(2020, 8, 10), 'description': "Belarusian protests"},
    {'start_date': dt.datetime(2020, 8, 20), 'end_date': dt.datetime(2020, 8, 22),
     'description': "Poisoning of Navalny"},
    {'start_date': dt.datetime(2020, 9, 27), 'end_date': dt.datetime(2020, 9, 27), 'description': "2nd Karabakh War"},
    {'start_date': dt.datetime(2020, 11, 3), 'end_date': dt.datetime(2020, 11, 3), 'description': "President Biden"},
    {'start_date': dt.datetime(2021, 1, 6), 'end_date': dt.datetime(2021, 1, 7), 'description': "Capitol attack"},
    {'start_date': dt.datetime(2021, 1, 17), 'end_date': dt.datetime(2021, 1, 17), 'description': "Navalny's return"},
    {'start_date': dt.datetime(2021, 1, 23), 'end_date': dt.datetime(2021, 1, 23),
     'description': "Pro-Navalny protests"},
    {'start_date': dt.datetime(2021, 5, 23), 'end_date': dt.datetime(2021, 5, 23),
     'description': "Belarusian Flight 4978"},
    {'start_date': dt.datetime(2021, 8, 13), 'end_date': dt.datetime(2021, 8, 19),
     'description': "Taliban is seizing power"},
    {'start_date': dt.datetime(2021, 10, 26), 'end_date': dt.datetime(2021, 10, 26),
     'description': "Merkel's resignation"},
    {'start_date': dt.datetime(2021, 11, 25), 'end_date': dt.datetime(2021, 11, 25),
     'description': "Listvyazhnaya mine"},
    {'start_date': dt.datetime(2021, 12, 8), 'end_date': dt.datetime(2021, 12, 8), 'description': "Olaf Scholz"},
)

stop_words = stopwords.words('russian')
stop_words.extend(['что', 'это', 'так',
                   'вот', 'быть', 'как',
                   'в', '—', 'к', 'за', 'из', 'из-за',
                   'на', 'ок', 'кстати',
                   'который', 'мочь', 'весь',
                   'еще', 'также', 'свой',
                   'ещё', 'самый', 'ул', 'комментарий',
                   'английский', 'язык', 'года', 'году'])
