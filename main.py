import yfinance as yf
import matplotlib.pyplot as plt
from datetime import date

from sources import get_my_portfolio
from strategy.sma import get_sma_data, draw_sma
from strategy.macd import get_macd_data, draw_macd

plt.style.use('fivethirtyeight')
yf.pdr_override()

start_date = date(2017, 8, 4)
end_date = date.today()
print(end_date)

stock_symbol = input('Enter stock symbol:')
stock_symbols = [stock_symbol]

data = get_my_portfolio('moex', stock_symbols, start_date, end_date)

sma_data = get_sma_data(data)

draw_sma(sma_data, stock_symbols, start_date, end_date)

macd_data = get_macd_data(sma_data)

draw_macd(macd_data, stock_symbols)