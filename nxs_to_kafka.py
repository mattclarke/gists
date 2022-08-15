import json
import time

import h5py
from streaming_data_types import serialise_ev42
from confluent_kafka import Producer
import numpy as np
from matplotlib import pyplot as plt
from fast_histogram import histogram1d

HEIGHT = 1152
WIDTH = 128
BROKER = 'localhost:9092'
OUTPUT_TOPIC = "FREIA_detector"

config = {"bootstrap.servers": BROKER}
producer = Producer(**config)

CONFIG_JSON = {
    "cmd": "config",
    "histograms": [
        {
            "type": "dethist",
            "data_brokers": ["localhost:9092"],
            "data_topics": ["FREIA_detector"],
            "tof_range": [0, 100000000],
            "det_range": [0, WIDTH * HEIGHT],
            "width": WIDTH,
            "height": HEIGHT,
            "topic": "local_visualisation",
            "id": "some_id"
        }
    ]
}

producer.produce("local_jbi_commands", bytes(json.dumps(CONFIG_JSON), "utf-8"))
producer.flush()

hdf = h5py.File('dmc_events.nxs', 'r')

hist = histogram1d(
    [],
    bins=WIDTH * HEIGHT, range=(0, WIDTH * HEIGHT)
)

for i, t0 in enumerate(hdf['instrument/DEMO/data/event_time_zero']):
    start = hdf['instrument/DEMO/data/event_index'][i]
    if i + 1 < len(hdf['instrument/DEMO/data/event_index']):
        end = hdf['instrument/DEMO/data/event_index'][i + 1]
        ids = hdf['instrument/DEMO/data/event_id'][start:end]
        offsets = hdf['instrument/DEMO/data/event_time_offset'][start:end]
    else:
        ids = hdf['instrument/DEMO/data/event_id'][start:]
        offsets = hdf['instrument/DEMO/data/event_time_offset'][start:]

    hist += histogram1d(ids, bins=WIDTH * HEIGHT, range=(0, WIDTH * HEIGHT))

    buf = serialise_ev42('from_file', i, t0, offsets, ids)
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
