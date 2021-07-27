__all__ = ['getBestTradingDay']

# libraries
import os
import requests
import datetime
import pdb

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
    baseUrl = 'https://api.polygon.io/v2/aggs/ticker/{stocksTicker}/range/{multiplier}/{timespan}/{from}/{to}?adjusted=true&sort=asc&apiKey={apiKey}'
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

    # best trading day
    df['amountMonthRank'] = df.groupby(groupCols)['l'].rank(method='dense')
    df['isLowestOfMonth'] = (df['amountMonthRank'] == 1) * 1

    dfBest = df.groupby('tradingDayOfMonth', as_index=False)\
        .agg({'isLowestOfMonth': 'sum'})\
        .sort_values('isLowestOfMonth', ascending=False)


    return dfBest



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker')
    args = parser.parse_args()
    print(args)
    df = getBestTradingDay(args.ticker, '2019-07-01', '2021-07-01')

    print(df.head())



