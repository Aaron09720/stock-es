"""Create price index"""
from es_client import es_client

def create_price_index() -> str:
    """Create price index."""
    if es_client.indices.exist(index='history-prices-daily'):
        msg = '\"history-prices-daily\" 已經存在'
        return msg

    price_index = {
        "mappings" : {
            "properties" : {
                "close" : {"type" : "float"},
                "date" : {"type" : "date"},
                "high" : {"type" : "float"},
                "low" : {"type" : "float"},
                "open" : {"type" : "float"},
                "stock_id" : {
                    "type" : "text",
                    "fields" : {
                        "keyword" : {
                            "type" : "keyword",
                            "ignore_above" : 256}}
                },
                "stock_name" : {"type" : "text",},
                "trade_volume" : {"type" : "long"},
                "transaction" : {"type" : "long"},
                "trade_value" : {"type" : "long"},
            }
        }
    }
    es_client.indices.create(index='history-prices-daily', body=price_index)

    msg = '\"history-prices-daily\" 已建立完成'
    return msg

if __name__ == '__main__':
    msg = create_price_index()
    print(msg)