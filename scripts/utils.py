import pandas as pd
import json, requests
from io import StringIO
import streamlit as st

api_url = "http://127.0.0.1:8000"

# @st.cache_data
def get_df_from_handlers_response(handler: str) -> pd.DataFrame:
    """Converts json received from API to dataframe"""
    handler_url = f"{api_url}/news/{handler}"
    # print(handler_url)
    response = requests.get(handler_url).json()
    json_dump = json.dumps(response)
    df = pd.read_json(StringIO(json_dump))
    return df




if __name__ == "__main__":
    # df = get_df_from_handlers_response("last_quota")
    # print(df.head())
    test_url = f"{api_url}/api/generate"
    response = requests.post('{"model": "llama2", "prompt": "Why is the sky blue?"}')
