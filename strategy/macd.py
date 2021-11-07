import numpy as np
import pandas as pd
import yfinance as yf
import pandas_ta as ta
import matplotlib.pyplot as plt
from draw import get_axis

plt.style.use('fivethirtyeight')
yf.pdr_override()


def get_macd_concat_data(data):
    return pd.concat([data, ta.macd(data['close'])], axis=1).reindex(data.index)


def macd_strategy(data, risk):
    result = data
    macd_buy = []
    macd_sell = []
    position = False

    for i in range(0, len(data)):
        if data['MACD_12_26_9'][i] > data['MACDs_12_26_9'][i]:
            macd_sell.append(np.nan)
            if not position:
                macd_buy.append(data['close'][i])
                position = True
            else:
                macd_buy.append(np.nan)
        elif data['MACD_12_26_9'][i] < data['MACDs_12_26_9'][i]:
            macd_buy.append(np.nan)
            if position:
                macd_sell.append(data['close'][i])
                position = False
            else:
                macd_sell.append(np.nan)
        elif position == True and data['close'][i] < macd_buy[-1] * (1 - risk):
            macd_sell.append(data["close"][i])
            macd_buy.append(np.nan)
            position = False
        elif position == True and data['close'][i] < data['close'][i - 1] * (1 - risk):
            macd_sell.append(data["close"][i])
            macd_buy.append(np.nan)
            position = False
        else:
            macd_buy.append(np.nan)
            macd_sell.append(np.nan)

    result['MACD_Buy_Signal_price'] = macd_buy
    result['MACD_Sell_Signal_price'] = macd_sell
    return result


def calc_macd_color(data):
    macd_color = []
    for i in range(0, len(data)):
        if data['MACDh_12_26_9'][i] > data['MACDh_12_26_9'][i - 1]:
            macd_color.append(True)
        else:
            macd_color.append(False)
    return macd_color


def get_data_with_indicators(data):
    data['positive'] = calc_macd_color(data)
    return data


def get_macd_data(data):
    macd_data = get_macd_concat_data(data)
    result = macd_strategy(macd_data, 0.025)
    return get_data_with_indicators(result)


def draw_macd(data, stocksymbols):
    plt.rcParams.update({'font.size': 10})
    ax1 = get_axis(stocksymbols, 'MACD')
    ax1.plot('close', data=data, label='close Price', linewidth=0.5, color='blue')
    ax1.scatter(data.index, data['MACD_Buy_Signal_price'], color='green', marker='^', alpha=1)
    ax1.scatter(data.index, data['MACD_Sell_Signal_price'], color='red', marker='v', alpha=1)
    ax1.legend()
    ax1.grid()
    ax1.set_xlabel('Date', fontsize=8)


    ax2 = plt.subplot2grid((14, 12), (10, 0), rowspan=6, colspan=14)
    ax2.set_ylabel('MACD', fontsize=8)
    ax2.plot('MACD_12_26_9', data=data, label='MACD', linewidth=0.5, color='blue')
    ax2.plot('MACDs_12_26_9', data=data, label='signal', linewidth=0.5, color='red')
    ax2.bar(data.index, 'MACDh_12_26_9', data=data, label='Volume', color=data.positive.map({True: 'g', False: 'r'}),
            width=1, alpha=0.8)
    ax2.axhline(0, color='black', linewidth=0.5, alpha=0.5)
    ax2.grid()
    plt.show()
