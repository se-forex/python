import time
import json
import requests
from datetime import datetime

MARKET = 'USDT-BTC'

def get_ticks():
    chart_data = {}
    # Получаем готовые данные свечей
    res = requests.get("https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName=" + MARKET + "&tickInterval=hour")
    for item in json.loads(res.text)['result']:
        try:
            dt_obj = datetime.strptime(item['T'], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            dt_obj = datetime.strptime(item['T'], '%Y-%m-%dT%H:%M:%S')
        ts = int(time.mktime(dt_obj.timetuple()))
        if not ts in chart_data:
            chart_data[ts] = {'open': float(item['O']), 'close': float(item['C']), 'high': float(item['H']), 'low': float(item['L'])}

    # Добираем недостающее
    res = requests.get("https://bittrex.com/api/v1.1/public/getmarkethistory?market=" + MARKET)
    for trade in reversed(json.loads(res.text)['result']):
        try:
            dt_obj = datetime.strptime(trade['TimeStamp'], '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            dt_obj = datetime.strptime(item['T'], '%Y-%m-%dT%H:%M:%S')
            
        ts = int((time.mktime(dt_obj.timetuple())/1800))*1800 # округляем /60*60 - минуты (час 3600)
        if not ts in chart_data:
            chart_data[ts] = {'open': 0, 'close': 0, 'high': 0,'low': 0}

        chart_data[ts]['close'] = float(trade['Price'])

        if not chart_data[ts]['open']:
            chart_data[ts]['open'] = float(trade['Price'])

        if not chart_data[ts]['high'] or chart_data[ts]['high'] < float(trade['Price']):
            chart_data[ts]['high'] = float(trade['Price'])

        if not chart_data[ts]['low'] or chart_data[ts]['low'] > float(trade['Price']):
            chart_data[ts]['low'] = float(trade['Price'])

    return chart_data

# Выведем результат, посмотрим - работаем по времени биржи
chart_data = get_ticks()
for item in sorted(chart_data):
    print(datetime.fromtimestamp(item),chart_data[item])
