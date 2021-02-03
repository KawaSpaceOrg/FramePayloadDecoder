import datetime, os
from elasticsearch import Elasticsearch

es_hosts =  [os.getenv('ES_HOST1'),os.getenv('ES_HOST2'),os.getenv('ES_HOST3')]

es = Elasticsearch(
    es_hosts,
    http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD1')),
    sniff_on_start=True
)

