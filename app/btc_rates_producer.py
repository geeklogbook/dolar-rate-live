import os
import time
import requests
import json
from datetime import datetime, timezone
from confluent_kafka import Producer

KAFKA_BROKER = "kafka:9092"
KAFKA_TOPIC = "bitcoin-data"

producer = Producer({"bootstrap.servers": KAFKA_BROKER})

API_URL = 'https://criptoya.com/api/BTC/USD'

def fetch_and_send_data():
    try:
        response = requests.get(API_URL, headers={'Content-Type': 'application/json'})
        response.raise_for_status()
        data = response.json()
        data["time"] = datetime.now(timezone.utc).isoformat()
        json_data = json.dumps(data)
        producer.produce(KAFKA_TOPIC, key=str(time.time()), value=json_data)
        producer.flush()  
        print(f"Mensaje enviado a Kafka: {json_data}")

    except requests.exceptions.RequestException as e:
        print(f"Error en la API: {e}")
    except Exception as e:
        print(f"Error al enviar a Kafka: {e}")

if __name__ == "__main__":
    while True:
        fetch_and_send_data()
        time.sleep(10)
