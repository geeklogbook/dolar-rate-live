from confluent_kafka import Consumer

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['quickstart-events'])

print("Listening for messages...")
while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print(f"Error: {msg.error()}")
        continue
    print(f"Consumed: {msg.value().decode('utf-8')}")  