from confluent_kafka import Producer

conf = {'bootstrap.servers': 'kafka:9092'}
producer = Producer(conf)

topic = 'quickstart-events'

messages = ["This is my first event", "This is my second event"]
for message in messages:
    producer.produce(topic, value=message)
    print(f"Produced: {message}")

producer.flush()