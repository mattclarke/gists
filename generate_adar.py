import datetime
import time

import matplotlib.image as mpimg
from confluent_kafka import Producer
from matplotlib.cbook import get_sample_data
from streaming_data_types import serialise_ADAr

OUTPUT_TOPIC = "local_camera"
BROKER = "localhost:9092"

img = mpimg.imread(get_sample_data("grace_hopper.jpg"))
img = img[:, :, 0].copy()
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

config = {"bootstrap.servers": BROKER, "message.max.bytes": 100_000_000}
producer = Producer(**config)

while True:
    buffer = serialise_ADAr("grace", int(time.time()), datetime.datetime.now(),
                            img)
    producer.produce(OUTPUT_TOPIC, buffer)
    producer.flush()
    time.sleep(5)

