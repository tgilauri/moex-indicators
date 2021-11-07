import yfinance as yf
import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')
yf.pdr_override()


def get_axis(stocksymbols, signal):
    fig, ax1 = plt.subplots(figsize=(14, 8))
    fig.suptitle(stocksymbols[0]+' ' + signal, fontsize=10, backgroundcolor='blue', color='white')
    ax1 = plt.subplot2grid((14, 8), (0, 0), rowspan=8, colspan=14)
    ax1.set_ylabel('Price in ₨')

    return ax1
