import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
from draw import get_axis

plt.style.use('fivethirtyeight')
yf.pdr_override()


def prepare_data(data):
    data['SMA 30'] = ta.sma(data['close'], 30)
    data['SMA 100'] = ta.sma(data['close'], 100)
    return data


# SMA BUY SELL
# Function for buy and sell signal
def get_signals(data):
    sma_buy = []
    sma_sell = []
    position = False

    for i in range(len(data)):
        if data['SMA 30'][i] > data['SMA 100'][i]:
            if not position:
                sma_buy.append(data['close'][i])
                sma_sell.append(np.nan)
                position = True
            else:
                sma_buy.append(np.nan)
                sma_sell.append(np.nan)
        elif data['SMA 30'][i] < data['SMA 100'][i]:
            if position:
                sma_buy.append(np.nan)
                sma_sell.append(data['close'][i])
                position = False
            else:
                sma_buy.append(np.nan)
                sma_sell.append(np.nan)
        else:
            sma_buy.append(np.nan)
            sma_sell.append(np.nan)
    return pd.Series([sma_buy, sma_sell])


def get_sma_data(data):
    result = data
    sma_data = prepare_data(data)
    result['Buy_Signal_price'], result['Sell_Signal_price'] = get_signals(sma_data)
    return result


def draw_sma(data, stocksymbols, start_date, end_date):
    ax = get_axis(stocksymbols, 'SMA')
    ax.plot(data['close'], label=stocksymbols[0], linewidth=0.5, color='blue', alpha=0.9)
    ax.plot(data['SMA 30'], label='SMA30', alpha=0.85)
    ax.plot(data['SMA 100'], label='SMA100', alpha=0.85)
    ax.scatter(data.index, data['Buy_Signal_price'], label='Buy', marker='^', color='green', alpha=1)
    ax.scatter(data.index, data['Sell_Signal_price'], label='Sell', marker='v', color='red', alpha=1)
    ax.set_title(stocksymbols[0] + " Price History with buy and sell signals", fontsize=10, backgroundcolor='blue',
                 color='white')
    ax.set_xlabel(f'{start_date} - {end_date}', fontsize=18)
    ax.set_ylabel('close Price INR (₨)', fontsize=18)
    legend = ax.legend()
    ax.grid()
    #plt.tight_layout()
    plt.show()
