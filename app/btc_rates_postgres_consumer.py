import json
from confluent_kafka import Consumer, KafkaException
import psycopg2


KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "bitcoin-data"
KAFKA_GROUP_ID = "postgres-saver"
POSTGRES_HOST =  "postgres"
POSTGRES_PORT = "5432"
POSTGRES_DB = "rates"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

consumer = Consumer({
    "bootstrap.servers": KAFKA_BROKER,
    "group.id": KAFKA_GROUP_ID,
    "auto.offset.reset": "earliest"
})

consumer.subscribe([KAFKA_TOPIC])

def get_db_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

def save_to_postgres(data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO bitcoin (data, created_at) 
            VALUES (%s, NOW())
        """, (json.dumps(data),))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"Guardado en PostgreSQL: {data.get('time', 'unknown')}")
        
    except Exception as e:
        print(f"Error al guardar en PostgreSQL: {e}")

if __name__ == "__main__":
    print("Esperando mensajes de Kafka para PostgreSQL")
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
        save_to_postgres(data)
