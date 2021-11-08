import pandas_datareader.data as web


def prepare_data(data):
    result = data
    key = 'CLOSE' if 'CLOSE' in data else 'Close'
    tmp = data[key]
    del result[key]
    result['close'] = tmp
    return result


def get_my_portfolio(stocks, start, end):
    if len(stocks) == 0:
        raise Exception('No symbols available')
    result = web.get_data_moex(stocks, start=start, end=end)
    return prepare_data(result)
