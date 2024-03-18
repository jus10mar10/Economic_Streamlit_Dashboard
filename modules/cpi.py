import requests
import json
import pandas as pd
from datetime import datetime
import os
import streamlit as st

def api_key():
    try:
        api_key = os.environ.get('CPI_API_KEY')
    except:
        api_key = st.secrets("CPI_API_KEY")
    return api_key

def get_cpi_index(start_year: str = None, end_year: str = None):
    api_key = api_key()
    if start_year is None:
        start_year = datetime.now().year
    if end_year is None:
        end_year = int(start_year) - 5
        end_year = str(end_year)

    headers = {'Content-type': 'application/json'}
    data = json.dumps({"seriesid": ['CUUR0000SA0'],"startyear":"2015", "endyear":"2024", "registrationkey": api_key})
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
    json_data = json.loads(p.text)
    df = pd.DataFrame(json_data['Results']['series'][0]['data'])
    df = df.sort_index(ascending=False)
    df['month'] = [x[1:] for x in df['period']]
    df['year-month'] = df['year'] + '-' + df['month']
    df.index = pd.to_datetime(df['year-month'])
    df['value'] = df['value'].astype(float)
    return df[['year-month', 'year', 'month', 'periodName', 'latest', 'value']]
    