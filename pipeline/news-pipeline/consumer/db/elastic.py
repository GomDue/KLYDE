from db.connection import get_elastic_conn

def insert_elasticsearch(data):
    es = get_elastic_conn()
    
    index_name = "news"
    es_doc = {
        "title":      data["title"],
        "content":    data["content"],
        "writer":     data["writer"],
        "category":   data["category"],
        "keywords":   data["keywords"],
        "write_date": data["write_date"]
    }
    es.update(
        index=index_name,
        id=data["url"],
        body={
            "doc": es_doc,
            "doc_as_upsert": True
        }
    )
