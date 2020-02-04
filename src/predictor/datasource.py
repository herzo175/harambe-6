import requests

from iexfinance.stocks import get_historical_data 

from config import config

def get_time_series_daily(symbol, start, end, apikey=config.STATIC_CONFIG.get_value("IEX_KEY")):
    data = get_historical_data(symbol, start, end, token=apikey, close_only=True)
    return {date: {'close': data[date]['close']} for date in data}
