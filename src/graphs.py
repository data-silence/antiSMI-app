import plotly.express as px
import pandas as pd
import streamlit as st

translation_countries = {'Russian': 'Россия', 'Ukranian': 'Украина', 'Non Ukranian': 'неУкраина'}


def draw_countries_type_pie(df: pd.DataFrame, filter: str):
    category = 'country'
    data_frame = pd.DataFrame(df[category][df[category] != ''].value_counts(), columns=['count'])
    match filter:
        case 'Exclude Russia':
            data_frame = data_frame.query(f"{category} != 'Россия'")
        case _:
            pass
    fig = px.pie(data_frame=data_frame, values='count', names=data_frame.index, height=600, hole=.2)
    fig.update_traces(textposition="inside", textinfo='value+label')
    # fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)

def draw_countries_pie(df: pd.DataFrame, country: str):
    rus_country_name = translation_countries[country]
    match rus_country_name:
        case 'неУкраина':
            data_frame = pd.DataFrame(df['settlement_name'][df['region'] == rus_country_name].value_counts(), columns=['count'])
        case _:
            data_frame = pd.DataFrame(df['settlement_name'][(df['country'] == rus_country_name) & (df['settlement_name'] != '')].value_counts(), columns=['count'])
    # data_frame = data_frame['settlement_name'][data_frame['country'] == country]
    fig = px.pie(data_frame=data_frame, values='count', names=data_frame.index, height=600, hole=.3, title=f'Number of media agencies in the {country} by city')
    fig.update_traces(textposition="inside", textinfo='value+label')
    # fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)


def draw_region_barchart(df: pd.DataFrame, country: str):
    rus_country_name = translation_countries[country]
    data_frame = pd.DataFrame(df['settlement_name'][(df['country'] == rus_country_name) & (df['settlement_name'] != '') & (df['settlement_type'] == 'город')].value_counts()[:22], columns=['count'])
    match rus_country_name:
        case 'Россия':
            data_frame = data_frame.query('settlement_name != "Москва"').query('settlement_name != "Санкт-Петербург"')
        case 'Украина':
            data_frame = data_frame.query('settlement_name != "Киев"')
    fig = px.bar(data_frame=data_frame, y='count', x=data_frame.index, text='count', height=600, color=data_frame.index, title=f"Largest {country} cities by number of news agencies exclude capitals", labels={'settlement_name': 'city', 'count': 'numbers of news agencies'})
    fig.update_traces(textposition="outside")
    # fig.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)