import yfinance as yf
import pandas_datareader.data as web
import matplotlib.pyplot as plt
from datetime import date

from strategy.bb import get_bb_data, draw_bb
from strategy.sma import get_sma_data, draw_sma
from strategy.macd import get_macd_data, draw_macd

plt.style.use('fivethirtyeight')
yf.pdr_override()

stocksymbols = ['SBER']
start_date = date(2017, 8, 4)
end_date = date.today()
print(end_date)

sources = {
    'moex': {
        'request': web.get_data_moex,
        'symbols': {
            'SBER': 'SBER'
        }
    },
    'yahoo': {
        'request': web.get_data_yahoo,
        'symbols': {
            'SBER': 'SBRCY'
        }
    }
}


def prepare_data(data):
    result = data
    result['close'] = data['CLOSE'] if 'CLOSE' in data else data['Close']
    return result


def get_my_portfolio(source, stocks=stocksymbols, start=start_date, end=end_date):
    request = sources[source]['request']
    symbols = list(map(lambda symbol: sources[source]['symbols'][symbol], stocks))
    result = request(symbols, start=start, end=end)
    return prepare_data(result)


data = get_my_portfolio('moex', stocksymbols)

sma_data = get_sma_data(data)

draw_sma(sma_data, stocksymbols, start_date, end_date)

macd_data = get_macd_data(sma_data)

draw_macd(macd_data, stocksymbols)

bb_data = get_bb_data(macd_data)

draw_bb(bb_data, stocksymbols)
