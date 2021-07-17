__all__ = ['getBestTradingDay']

# libraries
import os
import requests
import numpy as np
import pandas as pd
from dotenv import load_dotenv


def getBestTradingDay(ticker, dateFrom, dateTo, apiKey='polygonKey'):
    '''
    find the best trading day of the month to consistently trade a stock

    inputs
        ticker: symbol for the stock
        polygonKey: api key key in .env file
    '''

    # load credentials
    load_dotenv()
    apiKey = os.environ[apiKey]

    # initialize input params
    baseUrl = 'https://api.polygon.io/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}?adjusted=true&sort=asc&limit=120&apiKey={apiKey}'
    params = {
        'stocksTicker': ticker,
        'multiplier': 1,
        'timespan': 'day',
        'from': dateFrom,
        'to': dateTo,
        'apiKey': apiKey
    }
    url = baseUrl.format(**params)

    # get data
    r = requests.get(url)
    data = r.json()

    # format data
    df = pd.DataFrame(data['results'])
    df['ticker'] = data['ticker']
    df['date'] = pd.to_datetime(df['t'], unit='ms').dt.floor('D')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month


    # compute trading day of month
    groupCols = ['ticker', 'year', 'month']
    df['tradingDayOfMonth'] = df.groupby(groupCols)['date'].rank(method='dense')

    print(df.head())

def main():
    getBestTradingDay('TSLA', '2021-01-01', '2021-06-01')

if __name__ == '__main__':
    main()
