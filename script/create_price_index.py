from elasticsearch import Elasticsearch

def create_price_index():
    """Create price index."""
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

if __name__ == '__main__':
    create_price_index()