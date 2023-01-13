import time

from confluent_kafka import Producer

config = {"bootstrap.servers": "localhost:9092"}
producer = Producer(**config)

message = f'hello from {time.time_ns()}'
producer.produce("test_topic", message.encode())
producer.flush()
