import time

import matplotlib.pyplot as plt
import numpy as np
from confluent_kafka import Consumer, TopicPartition
from streaming_data_types import deserialise_ADAr

TOPIC = "ymir_camera"
BROKER = "10.100.1.19:9092"

consumer = Consumer(
    {
        "bootstrap.servers": BROKER,
        "group.id": f"consumer-{time.time_ns()}",
        "auto.offset.reset": "latest",
    }
)

metadata = consumer.list_topics(TOPIC)
if TOPIC not in metadata.topics:
    raise Exception("Topic does not exist")

topic_partitions = [
    TopicPartition(TOPIC, p) for p in metadata.topics[TOPIC].partitions
]

consumer.assign(topic_partitions)

while (msg := consumer.poll(timeout=0.5)) is None:
    pass

result = deserialise_ADAr(msg.value())

fig = plt.figure(1)
x, y = np.meshgrid(list(range(result.data.shape[0] + 1)), list(range(result.data.shape[1] + 1)))
ax = fig.add_subplot(111)
ax.pcolormesh(x, y, result.data.T)
plt.show()
