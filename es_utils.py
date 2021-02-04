import datetime, os
from elasticsearch import Elasticsearch

es = Elasticsearch(
    [os.getenv('ES_HOST')],
    http_auth=(os.getenv('ES_USER'), os.getenv('ES_PASSWORD')),
    sniff_on_start=True
)

