# from datetime import datetime
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow.providers.elasticsearch.hooks.elasticsearch import ElasticsearchHook

# def fetch_updated_data_from_postgres(last_run_time=None):
#     postgres_hook = PostgresHook(postgres_conn_id="postgres_news") 
    
#     sql = """
#     SELECT * FROM your_table
#     WHERE updated_at > %s
#     """
    
#     updated_data = postgres_hook.get_records(sql, parameters=(last_run_time,))
    
#     return updated_data

# def sync_data_to_elasticsearch(updated_data):
#     es_hook = ElasticsearchHook(elasticsearch_conn_id="elasticsearch_connection") 
#     es_client = es_hook.get_conn()
#     index_name = "news"
    
#     for record in updated_data:
#         try:
#             doc_id = record[0] 
#             document = {
#                 "title": record[1],
#                 "content": record[2], 
#                 "updated_at": record[3],
#             }

#             es_client.update(index=index_name, id=doc_id, body={"doc": document, "doc_as_upsert": True})
#             print(f"Updated document {doc_id} in Elasticsearch.")
#         except Exception as e:
#             print(f"[ES Update Failed] Error updating document {doc_id}: {e}")

#     print(f"Updated {len(updated_data)} documents in Elasticsearch.")
