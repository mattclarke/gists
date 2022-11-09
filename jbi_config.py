import json
import time

from streaming_data_types import serialise_ev42
from confluent_kafka import Producer
import numpy as np
from matplotlib import pyplot as plt
from fast_histogram import histogram1d


HEIGHT = 51
WIDTH = 60
BROKER = 'localhost:9092'
OUTPUT_TOPIC = "local_detector"


config = {"bootstrap.servers": BROKER}
producer = Producer(**config)


CONFIG_JSON = {
    "cmd": "config",
    "start": 1667978333812,
    "stop": 1667978433812,
    "histograms": [
        {
            "type": "dethist",
            "data_brokers": ["localhost:9092"],
            "data_topics": [OUTPUT_TOPIC],
            "tof_range": [0, 100000000],
            "det_range": [0, 100000000],
            "width": WIDTH,
            "height": HEIGHT,
            "topic": "local_visualisation",
            "id": "some_id",
            "start": 1667976659961,
        }
    ]
}

producer.produce("local_jbi_commands", bytes(json.dumps(CONFIG_JSON), "utf-8"))
producer.flush()
