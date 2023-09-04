import datetime
import time

from confluent_kafka import Producer
from streaming_data_types import serialise_tdct

OUTPUT_TOPIC = "local_camera"
BROKER = "localhost:9092"

config = {"bootstrap.servers": BROKER, "message.max.bytes": 100_000_000}
producer = Producer(**config)

while True:
    buffer = serialise_tdct("tdct", [time.time_ns()])
    producer.produce(OUTPUT_TOPIC, buffer)
    producer.flush()
    time.sleep(1)
