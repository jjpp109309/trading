# %%
import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# %%
today = str(pd.Timestamp('today').date())


# %%
def get_daily_data(ticker, date_from, date_to=today, **kwargs):
    params = '&'.join(key + '=' + value for key, value in kwargs.items())
    api_key = os.environ['polygon']

    url = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{date_from}/{date_to}?apiKey={api_key}' + params

    r = requests.get(url)
    data = r.json()

    df = pd.DataFrame(data['results'])

    df['t'] = pd.to_datetime(df['t'], unit='ms').dt.date
    df.insert(0, 'ticker', ticker)

    return df


# %%
def main():
    df_daily = get_daily_data('AAPL', '2021-08-01', '2021-08-31')
    print(df_daily.head())
    print(df_daily.tail())

    df_daily = get_daily_data('TSLA', '2021-08-01')
    print(df_daily.head())
    print(df_daily.tail())


if __name__ == '__main__':
    main()
