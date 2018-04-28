from elasticsearch import Elasticsearch


def index_biblio(docid, biblio):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.index(
        index='biblio',
        doc_type='_doc',
        id=docid,
        body=biblio
    )


def index_clms(docid, clms):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    es.index(
        index='clms',
        doc_type='_doc',
        id=docid,
        body=clms
    )