import requests
import json
import xmltodict
import pandas as pd
from datetime import datetime
import re


def pull_yield_curve_data(YYYYMM: str = None):
    '''
    YIELD CURVE DATA PULL
    FROM TREASURY.GOV

    In XML format, date values are in YYYYMM format.
    Date needs to be appended to end of string.
    '''
    # If no date is provided, use current date
    if YYYYMM == None:
        YYYYMM = datetime.now().strftime('%Y%m')
        
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    
    link = "https://home.treasury.gov/resource-center/data-chart-center/interest-rates/pages/xml?data=daily_treasury_yield_curve&field_tdr_date_value_month="
    
    # Pull data from treasury.gov
    response = requests.get(link + YYYYMM, headers=headers)
    # Convert XML to JSON
    decoded_response = response.content.decode('utf-8')
    # Convert JSON to dictionary
    response_json = json.loads(json.dumps(xmltodict.parse(decoded_response)))
    return response_json

def format_data(data: dict):
    # Extract data from dictionary
    entries = [data['feed']['entry'][i]['content']['m:properties'] for i in range(len(data['feed']['entry']))]
    # Get keys
    keys = list(entries[0].keys())

    data = {}
    
    # Create dictionary with date as key, for pandas dataframe
    for entry in entries:
        # data[date] = {'date': {maturity: yield}}
        date = entry['d:NEW_DATE']['#text']
        data[date] = {}
        for key in keys[1:-1]:
            data[date][key[5:]] = entry[key]['#text']
            
    df = pd.DataFrame(data)
    df.columns = pd.to_datetime(df.columns).strftime('%Y-%m-%d')
    df.index.name = 'term'
    df = df.astype(float) / 100
    return df

def year_ago_from_YYYMM(YYYYMM):
    YYYYMM = str(YYYYMM)
    year = int(YYYYMM[:4])
    last_year = str(year - 1)
    new_YYYYMM = last_year + YYYYMM[4:]
    data = yield_curve_data_pull(new_YYYYMM)
    data.columns = ['LAST YEAR (' + x +')' for x in data.columns]
    return data

def month_ago_from_YYYMM(YYYYMM):
    YYYYMM = str(YYYYMM)
    year = int(YYYYMM[:4])
    month = int(YYYYMM[4:])
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    new_YYYYMM = str(year) + str(month).zfill(2)
    data = yield_curve_data_pull(new_YYYYMM)
    data.columns = ['LAST MONTH (' + x +')' for x in data.columns]
    return data

def six_month_ago_from_YYYMM(YYYYMM):
    YYYYMM = str(YYYYMM)
    year = int(YYYYMM[:4])
    month = int(YYYYMM[4:])
    if month <= 6:
        year -= 1
        month = month + 6
    else:
        month -= 6
    new_YYYYMM = str(year) + str(month).zfill(2)
    data = yield_curve_data_pull(new_YYYYMM)
    data.columns = ['SIX MONTHS AGO (' + x +')' for x in data.columns]
    return data


def yield_curve_data_pull(YYYYMM: str = None):
    data = pull_yield_curve_data(YYYYMM)
    formatted_data = format_data(data)
    return formatted_data

def yield_curve_full_data_pull(YYYYMM: str = None):
    if YYYYMM == None:
        YYYYMM = datetime.now().strftime('%Y%m')
    
    current_data = yield_curve_data_pull(YYYYMM).iloc[:, -1:]
    current_day = current_data.columns[0].split('-')[-1]
    if int(current_day) > 28:
        current_day = '28'
        
    current_data.columns = ['LATEST (' + x +')' for x in current_data.columns]
    
    month_ago = month_ago_from_YYYMM(YYYYMM)
    # match day of month in current data
    month_ago = month_ago[[x for x in month_ago.columns if x.split('-')[-1] == current_day +')']]
    
    six_month_ago = six_month_ago_from_YYYMM(YYYYMM)
    six_month_ago = six_month_ago[[x for x in six_month_ago.columns if x.split('-')[-1] == current_day +')']]
    
    last_year_data = year_ago_from_YYYMM(YYYYMM)
    last_year_data = last_year_data[[x for x in last_year_data.columns if x.split('-')[-1] == current_day +')']]
    
    stacked = pd.concat([current_data, month_ago, six_month_ago, last_year_data], axis=1)
    
    # in this format 10YEAR seperate the num and title capitalization
    stacked.index = [re.sub(r'(\d+)([A-Z]+)', r'\1 \2', x) for x in stacked.index]
    
    return stacked
