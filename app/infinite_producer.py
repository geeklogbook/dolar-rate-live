from confluent_kafka import Producer
import random
import time

conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)

topic = 'infinite-events'

message_1 = 1

while True:
    message_to_stream = f"This is the message {message_1}"
    producer.produce(topic, value=message_to_stream)
    print(f"Produced: {message_to_stream}")
    producer.flush()
    time.sleep(10)  
    message_1 += 1

producer.flush()