import time

from confluent_kafka import Producer
from streaming_data_types import serialise_f144

OUTPUT_TOPIC = "test_topic"
BROKER = "localhost:9092"

config = {"bootstrap.servers": BROKER}
producer = Producer(**config)

try:
    while True:
        data = [123, 456, 789]
        time_ns = time.time_ns()
        buffer = serialise_f144("hello", data, time_ns)
        producer.produce(OUTPUT_TOPIC, buffer)
        producer.flush()
        time.sleep(0.5)
except:
    pass
