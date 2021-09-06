# %%
import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# %%
today = str(pd.Timestamp('today').date())


# %%
def daily_data(ticker: str, date_from: str, date_to: str=today, **kwargs)-> pd.DataFrame:

    params = '&'.join(key + '=' + value for key, value in kwargs.items())
    api_key = os.environ['polygon']

    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date_from}/{date_to}?apiKey={api_key}' + params

    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data['results'])
    col_names = {
        'v': 'volume',
        'vw': 'volume_weighted',
        'o': 'open',
        'c': 'close',
        'h': 'high',
        'l': 'low',
        'n': 'transactions'
    }
    df.rename(columns=col_names, inplace=True)

    df['date'] = pd.to_datetime(df['t'], unit='ms').dt.floor('D')

    df.insert(0, 'ticker', ticker)
    df.pop('t')

    return df


# %%
def main():
    df_daily = daily_data('AAPL', '2021-08-01', '2021-08-31')
    print(df_daily['date'].min(), df_daily['date'].max())
    df_daily = daily_data('TSLA', '2021-08-01')
    print(df_daily['date'].min(), df_daily['date'].max())
    print(df_daily.columns)

if __name__ == '__main__':
    main()
