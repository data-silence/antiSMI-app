import plotly.express as px
import pandas as pd
import streamlit as st
from plotly_calplot import calplot

from src.scripts import get_digit_from_tm

from src.constants import translation_countries


def draw_countries_pie(df: pd.DataFrame):
    type_filter = st.radio(
        "Select the type:",
        ['region', 'country'],
        horizontal=True, label_visibility='hidden'
    )

    border_filter = st.radio(
        "Do you want to see Russian agencies or only abroad agencies?",
        ['exclude Russia', 'with Russia'],
        horizontal=True, label_visibility='hidden'
    )

    if border_filter == 'exclude Russia':
        df = df.query(f"country != 'Россия'")

    data_frame = pd.DataFrame(df[type_filter][df[type_filter] != ''].value_counts(), columns=['count'])

    fig = px.pie(data_frame=data_frame, values='count', names=data_frame.index, height=600, hole=.3,
                 title=f'Russian-language media by {type_filter} [{border_filter}]')
    fig.update_traces(textposition="inside", textinfo='value+label')
    fig.update_layout(annotations=[
        dict(text=f'Total = {data_frame['count'].sum()}', x=0.5, y=0.5, font_size=16, showarrow=False)])
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def draw_cities_barchart(df: pd.DataFrame):
    country_filter = st.radio(
        "Select a country",
        ['russian', 'ukranian', 'non ukranian'],
        horizontal=True, label_visibility='hidden'
    )
    is_capitals = st.radio(
        "Do you need capitals?",
        ['exclude capitals', 'with capitals'],
        horizontal=True, label_visibility='hidden'
    )
    top_cities = st.slider('How many cities do you want to see?', 10, 100, 50, label_visibility='hidden')

    rus_country_name = translation_countries[country_filter]

    match rus_country_name:
        case 'неУкраина':
            data_frame = pd.DataFrame(df['settlement_name'][df['region'] == rus_country_name].value_counts(),
                                      columns=['count'])
        case _:
            data_frame = pd.DataFrame(df['settlement_name'][
                                          (df['country'] == rus_country_name) & (
                                                  df['settlement_name'] != '')].value_counts()[
                                      :top_cities], columns=['count'])

    if is_capitals == 'exclude capitals':
        data_frame = data_frame.query('settlement_name != "Москва"').query(
            'settlement_name != "Санкт-Петербург"').query('settlement_name != "Киев"')

    fig = px.bar(data_frame=data_frame, y='count', x=data_frame.index, text='count', height=600, color=data_frame.index,
                 title=f"{country_filter.title()} cities by number of russian news agencies [{is_capitals}]",
                 labels={'settlement_name': 'city', 'count': 'numbers of news agencies'})
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def draw_top_charts(df):
    key_features = (
        'type', 'rf_feds_subj', 'settlement_type', 'settlement_name', 'street', 'street_type', 'last', 'first')

    feature_dict = {'type': 'media type', 'rf_feds_subj': 'name of the region', 'settlement_type': 'settlement type',
                    'settlement_name': 'settlement name', 'street': 'street name', 'street_type': 'street type',
                    'last': 'editor last name', 'first': 'editor first name'}

    features_filter = st.radio(
        "Select category to get top 10 chart",
        [feature_dict[key] for key in key_features],
        horizontal=True
    )

    user_filter = [k for k, v in feature_dict.items() if v == features_filter][0]

    data_frame = pd.DataFrame(df[user_filter][df[user_filter] != ''].value_counts()[:10], columns=['count'])

    fig = px.bar(data_frame=data_frame, y='count', x=data_frame.index, text='count', height=600, color=data_frame.index,
                 labels={str(data_frame.index.names[0]): 'chart feature', 'count': 'numbers of news agencies'},
                 title=f'Top 10 by {features_filter}')
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def draw_tm_news_by_date(df):
    fig = px.bar(data_frame=df, y='count', x='date', height=600, title='News distribution by date')
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def draw_metrics():
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label='start date', value=get_digit_from_tm('min_date'))
    with col2:
        st.metric(label='news', value=f'{int(get_digit_from_tm('news_amount')):,}')
    with col3:
        st.metric(label='agencies', value=f'{int(get_digit_from_tm('agencies_amount')):,}')
    with col4:
        st.metric(label='categories', value=f'{int(get_digit_from_tm('categories_amount')):,}')
    with col5:
        st.metric(label='last date', value=get_digit_from_tm('max_date'))


def draw_calendar_heatmap(df: pd.DataFrame):
    st.write('Last year news distribution')
    fig = calplot(
        df.iloc[-365:, :],
        x="date",
        y="count",
        total_height=210,
        # dark_theme=True,
        # years_title=True,
        # month_lines_width=3,
        gap=0,
        colorscale="blues"
    )
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

# fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
