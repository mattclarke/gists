import json
import random
import time

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from confluent_kafka import Producer
from matplotlib.cbook import get_sample_data
from streaming_data_types import serialise_ev44

OUTPUT_TOPIC = "local_detector"
BROKER = "localhost:9092"

img = mpimg.imread(get_sample_data("grace_hopper.jpg"))
img = img[:, :, 0].copy()
print(f"x = {img.shape[0]}, y = {img.shape[1]}")
num_pixels = img.shape[0] * img.shape[1]

# Add horizontal guideline
for x in range(img.shape[1]):
    img[img.shape[0] // 2 - 1][x] = 0
    img[img.shape[0] // 2][x] = 0
    img[img.shape[0] // 2 + 1][x] = 0

# Add vertical guideline
for x in range(img.shape[0]):
    img[x][img.shape[1] // 2 - 1] = 0
    img[x][img.shape[1] // 2] = 0
    img[x][img.shape[1] // 2 + 1] = 0

hist_data = np.zeros([img.shape[0], img.shape[1]])

config = {"bootstrap.servers": BROKER}
producer = Producer(**config)

# uncomment this if you want to start just-bin-it histogramming
#
# CONFIG_JSON = {
#     "cmd": "config",
#     "input_schema": "ev44",
#     "output_schema": "hs01",
#     "histograms": [
#         {
#             "type": "dethist",
#             "data_brokers": [BROKER],
#             "data_topics": [OUTPUT_TOPIC],
#             "tof_range": [0, 100000000],
#             "det_range": [0, img.shape[0] * img.shape[1]],
#             "width": img.shape[1],
#             "height": img.shape[0],
#             "topic": "local_visualisation",
#             "id": "some_id",
#             "source": "grace",
#         }
#     ]
# }
#
# producer.produce("local_jbi_commands", bytes(json.dumps(CONFIG_JSON), "utf-8"))
# producer.flush()

try:
    while True:
        det_ids = []

        for _ in range(5000):
            pixel = random.randint(0, num_pixels - 1)
            row = pixel // img.shape[1]
            col = pixel % img.shape[1]
            chance = random.randint(0, 256)
            if chance < img[row][col]:
                hist_data[row][col] += 1
                det_ids.append(pixel)  # det ids start at 1

        time_ns = time.time_ns()
        buffer = serialise_ev44("grace", time_ns, [time_ns], [0], det_ids, det_ids)
        producer.produce(OUTPUT_TOPIC, buffer)
        producer.flush()
        time.sleep(0.5)
except:
    pass

fig = plt.figure(1)
x, y = np.meshgrid(list(range(img.shape[0] + 1)), list(range(img.shape[1] + 1)))
ax = fig.add_subplot(111)
ax.pcolormesh(x, y, hist_data.T)
plt.show()
