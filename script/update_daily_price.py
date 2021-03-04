"""Update daily price"""
import json
import requests

from datetime import datetime
from elasticsearch import Elasticsearch

from notify import notify


es_client = Elasticsearch()
parse_comma = (lambda num: num.replace(',', ''))

def update_daily_price():
    """Update daily price."""
    url = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL'
    response = requests.get(url)
    data = json.loads(response.text)

    # TODO: check fields sort
    if data['fields'] != ["證券代號", "證券名稱", "成交股數", "成交金額", "開盤價", "最高價", "最低價", "收盤價", "漲跌價差", "成交筆數"]:
        msg = "欄位格式錯誤"
        return msg
    
    documents = []
    _date = datetime.strftime(
        datetime.strptime(data['date'], '%Y%m%d'), '%Y-%m-%d')
    for item in data['data']:
        document = {}
        document['date'] = _date
        document['stock_id'] = item[0]
        document['stock_name'] = item[1]
        document['trade_volume'] = int(parse_comma(item[2]))
        document['trade_value'] = int(parse_comma(item[3]))
        document['open'] = float(parse_comma(item[4]))
        document['high'] = float(parse_comma(item[5]))
        document['low'] = float(parse_comma(item[6]))
        document['close'] = float(parse_comma(item[7]))
        document['transaction'] = int(parse_comma(item[9]))

        action = {}
        actionProperties = {}
        actionProperties["_id"] = f"{document['date']}-{document['stock_id']}"
        action["index"] = actionProperties
        documents.append(action)
        documents.append(document)

    result = es_client.bulk(body=documents, index='history-prices-daily')
    if len(result['item']) == len(data['data']):
        msg = '成功更新當日股價'
    else:
        msg = '資料更新筆數有誤'

    return msg


if __name__ == '__main__':
    notify_msg = update_daily_price()
    notify.send_notify_msg(notify_msg)
