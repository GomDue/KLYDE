from kafka import KafkaConsumer
import json

kafka_props = {
    'bootstrap_servers': 'localhost:9092',
    'group_id': 'consumer_group',
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
    'value_deserializer': lambda x: json.loads(x.decode('utf-8'))
}

consumer = KafkaConsumer("news", **kafka_props)

for msg in consumer:
    print(f"[Consumed] {msg.value}")
