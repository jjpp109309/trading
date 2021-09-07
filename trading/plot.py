import pandas as  pd
import matplotlib.pyplot as plt
from utilities import daily_data


def plot_daily_data(ticker: str, period: str='3M', price_type: str='c')-> None:
    '''
        plot ticker tiem series

        input
            ticker
            period: 1W, 1M, 3M, 6M, 1Y
            price_type: o(pen), h(igh), l(low), c(lose)
    '''

    price_type_parse = {
        'o': 'open',
        'h': 'high',
        'l': 'low',
        'c': 'close'
    }

    # period dates
    today = pd.Timestamp.today().date()
    date_from = str((today + pd.DateOffset(years=-1)).date())
    df = daily_data(ticker, date_from)

    # TODO: parse period input


    fig, ax = plt.subplots(figsize=(12, 8))
    pt = price_type_parse[price_type]
    ax.plot(df['date'], df[pt], 'C0', label=ticker)
    ax.set_xlabel('date')
    ax.set_ylabel(f'{pt} price')
    ax.set_title(f'{ticker}')
    ax.grid()

    plt.show()

def main():
    plot_daily_data('AAPL')

if __name__ == '__main__':
    main()
