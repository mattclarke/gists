import json
import time

from streaming_data_types import serialise_ev42
from confluent_kafka import Producer
import numpy as np
from matplotlib import pyplot as plt
from fast_histogram import histogram1d

HEIGHT = 3
WIDTH = 6
BROKER = 'localhost:9092'
OUTPUT_TOPIC = "local_detector"
FIRST_ID = 0


config = {"bootstrap.servers": BROKER}
producer = Producer(**config)


CONFIG_JSON = {
    "cmd": "config",
    "histograms": [
        {
            "type": "dethist",
            "data_brokers": ["localhost:9092"],
            "data_topics": [OUTPUT_TOPIC],
            "tof_range": [0, 100000000],
            "det_range": [FIRST_ID, 100000000],
            "width": WIDTH,
            "height": HEIGHT,
            "topic": "local_visualisation",
            "id": "some_id"
        }
    ]
}

producer.produce("local_jbi_commands", bytes(json.dumps(CONFIG_JSON), "utf-8"))
producer.flush()


hist = histogram1d([], bins=WIDTH * HEIGHT, range=(0, WIDTH * HEIGHT))

ids = []
ids.extend(([float(0 + FIRST_ID)] * 20))
ids.extend(([float(WIDTH - 1 + FIRST_ID)] * 30))
ids.extend(([float(WIDTH * HEIGHT - WIDTH + FIRST_ID)] * 40))
ids.extend(([float(WIDTH * HEIGHT - 1 + FIRST_ID)] * 50))

for i in range(100):
    hist += histogram1d(ids, bins=WIDTH * HEIGHT, range=(0, WIDTH * HEIGHT))

    buf = serialise_ev42('corners', i, 0, ids, ids)
    producer.produce(OUTPUT_TOPIC, buf)
    producer.flush()
    time.sleep(0.5)

hist2d, x_edges, y_edges = np.histogram2d(
            [],
            [],
            range=((0, WIDTH), (0, HEIGHT)),
            bins=(WIDTH, HEIGHT),
        )

for i, value in enumerate(hist):
    x = i % WIDTH
    y = i // WIDTH
    hist2d[x][y] = value

fig = plt.figure(1)
ax = fig.add_subplot(111)
x, y = np.meshgrid(x_edges, y_edges)
ax.pcolormesh(x, y, hist2d.T)
plt.show()
