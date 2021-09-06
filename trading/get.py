# %%
import requests
import os
import pdb
import pandas


_base_url = 'https://www.alphavantage.co/query?'

#%%
def parse_config(config: dict) -> str:
    return '&'.join(param+'='+value for param, value in config.items())

#%%
def dailey_adjusted(ticker: str)-> pandas.DataFrame:
    # api call params
    config = {
        'function': 'TIME_SERIES_DAILY_ADJUSTED',
        'apikey': os.environ['alphavantage'],
        'symbol': ticker.upper(),
        'datatype': 'json',
        'outputsize': 'full'
    }

    # request 
    url = _base_url + parse_config(config)
    r = requests.get(url)
    data = r.json()

    # parse data
    records = [
        (date, ) + tuple(record.values())
    for date, record in data['Time Series (Daily)'].items()]

    columns = [
        'date',
        'open',
        'high',
        'low',
        'close',
        'adjustedClose',
        'volume',
        'dividendAmount',
        'splitCoefficient'
    ]
    df = pandas.DataFrame.from_records(records, columns=columns)

    # data types
    df['date'] = pandas.to_datetime(df['date'], format='%Y-%m-%d')
    for col in columns[1:]:
        df[col] = df[col].astype('float')

    return df

# %%
if __name__ == '__main__':
    from dotenv import load_dotenv
    import pdb

    load_dotenv()
    df = dailey_adjusted('tsla')

    pdb.set_trace()

