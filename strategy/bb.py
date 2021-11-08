import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
from draw import get_axis

plt.style.use('fivethirtyeight')
yf.pdr_override()


def prepare_data(data):
    bb = ta.bbands(data['close'], length=20, std=2)
    data[bb.name] = bb
    return data


def strategy(data):
    bb_buy = []
    bb_sell = []
    position = False

    for i in range(len(data)):
        if data['close'][i] < data['BBL_20_2.0'][i]:
            if not position:
                bb_buy.append(data['close'][i])
                bb_sell.append(np.nan)
                position = True
            else:
                bb_buy.append(np.nan)
                bb_sell.append(np.nan)
        elif data['close'][i] > data['BBU_20_2.0'][i]:
            if position:
                bb_buy.append(np.nan)
                bb_sell.append(data['close'][i])
                position = False  # To indicate that I actually went there
            else:
                bb_buy.append(np.nan)
                bb_sell.append(np.nan)
        else:
            bb_buy.append(np.nan)
            bb_sell.append(np.nan)

    data['bb_Buy_Signal_price'] = bb_buy
    data['bb_Sell_Signal_price'] = bb_sell

    return data


def get_bb_data(data):
    bb_data = prepare_data(data)
    return strategy(bb_data)


def draw_bb(data, stocksymbols):
    # plot
    ax1 = get_axis(stocksymbols, 'Bollinger')
    ax1.plot(data['close'], label='close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['bb_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['bb_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)

    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax2.plot(data['BBM_20_2.0'], label='Middle', color='blue', alpha=0.35)  # middle band
    ax2.plot(data['BBU_20_2.0'], label='Upper', color='green', alpha=0.35)  # Upper band
    ax2.plot(data['BBL_20_2.0'], label='Lower', color='red', alpha=0.35)  # lower band
    ax2.fill_between(data.index, data['BBL_20_2.0'], data['BBU_20_2.0'], alpha=0.1)
    ax2.legend(loc='upper left')
    ax2.grid()
    plt.show()
