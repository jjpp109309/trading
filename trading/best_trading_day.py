__all__ = ['best_trading_day']

import pandas as pd
from utilities import daily_data


#%%
def best_trading_day(ticker: str, date_from: str, date_to: str)-> pd.DataFrame:
    '''
    find the best trading day of the month to consistently trade a stock

    '''

    df = daily_data(ticker, date_from, date_to)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month


    # compute trading day of month
    group_cols = ['ticker', 'year', 'month']
    df['trading_day_of_month'] = df.groupby(group_cols)['date'].rank(method='dense')

    # best trading day
    df['amount_month_rank'] = df.groupby(group_cols)['low'].rank(method='dense')
    df['is_lowest_of_month'] = (df['amount_month_rank'] == 1) * 1

    df_best = df\
        .groupby('trading_day_of_month', as_index=False)\
        .agg(**{'total_lowest_time': ('is_lowest_of_month', 'sum')})\
        .sort_values('total_lowest_time', ascending=False)


    return df_best



if __name__ == '__main__':
    import argparse


    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker')
    args = parser.parse_args()
    print(args)
    df = best_trading_day(args.ticker, '2019-07-01', '2021-08-31')

    print(df.head())



