import os, requests, json, csv, sys, time
import pandas as pd



def get_time_series_daily(key: str, symbol: str) -> list:
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&outputsize=full&apikey={}'.format(symbol, key)
    data = requests.get(url)
    if data.status_code == 200:
        data = json.loads(data.content)
        return data
    else:
        print('Error')
        return

def get_symbol_status(key: str):
    url = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={}'.format(key)
    data = requests.get(url)
    if data.status_code == 200:
        data = data.content.decode('utf-8')
        data = list(csv.reader(data.splitlines(), delimiter=','))
        data =  pd.DataFrame(data, columns=['symbol', 'name', 'exchange', 'assetType', 'ipodate', 'delistingdate', 'status'])
        data = data[data['assetType'] == 'Stock']
        return data
    else:
        print('Error')
        return


def get_company_details(key: str, symbol: str):
    url = 'https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}'.format(symbol, key)
    data = requests.get(url)
    if data.status_code == 200:
        data = json.loads(data.content)
        return data
    else:
        print('Error')
        return


# def main():
#     alpha_key = get_alphavantage_api_key()
#     symbols = get_symbol_status(key=alpha_key)
#     comp_data = {}
#     for symbol in symbols[0:5].symbol:
#         comp_data[symbol] = {}
#         comp_data[symbol]['info'] = get_company_details(key=alpha_key, symbol=symbol)
#         comp_data[symbol]['daily_ts'] = get_time_series_daily(key=alpha_key, symbol=symbol)
#         time.sleep(5)
#     # print(pd.DataFrame(comp_data))
#     for symbol in comp_data:
#         print(comp_data[symbol])
#         print('-------------------------------------------------------------------')

# if __name__ == '__main__':
#     main()