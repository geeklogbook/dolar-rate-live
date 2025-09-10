import os
import json
from confluent_kafka import Consumer, KafkaException
import boto3

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "bitcoin-data"
KAFKA_GROUP_ID = "minio-saver"
MINIO_ENDPOINT =  "http://data-lake:9000"
MINIO_ACCESS_KEY = "minio"
MINIO_SECRET_KEY = "minio123"
MINIO_BUCKET = "bitcoin-data"

s3_client = boto3.client(
    "s3",
    endpoint_url=MINIO_ENDPOINT,
    aws_access_key_id=MINIO_ACCESS_KEY,
    aws_secret_access_key=MINIO_SECRET_KEY
)

consumer = Consumer({
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": KAFKA_GROUP_ID,
    "auto.offset.reset": "earliest"
})

consumer.subscribe([KAFKA_TOPIC])

def create_bucket_if_not_exists():
    try:
        s3_client.head_bucket(Bucket=MINIO_BUCKET)
    except:
        s3_client.create_bucket(Bucket=MINIO_BUCKET)
        print(f"Bucket '{MINIO_BUCKET}' creado")

def save_to_minio(data):
    try:
        json_data = json.dumps(data)

        file_name = f"bitcoin_data_{data.get('time', 'unknown')}.json"

        s3_client.put_object(Bucket=MINIO_BUCKET, Key=file_name, Body=json_data)
        print(f"Guardado en MinIO: {file_name}")

    except Exception as e:
        print(f"Error al guardar en MinIO: {e}")

if __name__ == "__main__":
    print("Esperando mensajes de Kafka...")
    create_bucket_if_not_exists()
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaException._PARTITION_EOF:
                continue
            else:
                print(f"Error en Kafka: {msg.error()}")
                break
        data = json.loads(msg.value().decode("utf-8"))
        save_to_minio(data)
