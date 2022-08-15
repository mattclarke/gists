from confluent_kafka import Producer
import json
import time

CONFIG_JSON = {
    "cmd": "config",
    # "start": 1574837410000,
    # "stop": 1574840366000,
    "histograms": [
        {
            "type": "dethist",
            "data_brokers": ["localhost:9092"],
            "data_topics": ["FREIA_detector"],
            "tof_range": [0, 100000000],
            "det_range": [0, 147456],
            "width": 128,
            "height": 1152,
            "topic": "local_visualisation",
            "id": "some_id"
        }
        # {
        #     "type": "dethist",
        #     "data_brokers": ["localhost:9092"],
        #     "data_topics": ["grace_detector"],
        #     "tof_range": [0, 100000000],
        #     "det_range": [1, 307200],
        #     "width": 512,
        #     "height": 600,
        #     "topic": "local_visualisation",
        #     "id": "some_id"
        # }
        # {
        #     "type": "hist1d",
        #     "data_brokers": ["172.30.242.19:9092"],
        #     "data_topics": ["monitor"],
        #     "tof_range": [0, 100_000_000],
        #     "det_range": [0, 100_000_000],
        #     "num_bins": 100,
        #     "source": "Monitor_Adc0_Ch2",
        #     "topic": "hist_topic3",
        #     "id": "some_id1"
        # }
        # {
        #     "type": "hist2d",
        #     "data_brokers": ["172.30.242.27:9092"],
        #     "data_topics": ["monitor"],
        #     "tof_range": [0, 100000000],
        #     "det_range": [0, 100],
        #     "num_bins": 50,
        #     "topic": "hist-topic2",
        #     "id": "some_id3"
        # },
        # {
        #     "type": "dethist",
        #     "data_brokers": ["172.30.242.27:9092"],
        #     "data_topics": ["monitor"],
        #     "tof_range": [0, 100000000],
        #     "det_range": [1, 10_000],
        #     "width": 100,
        #     "height": 100,
        #     "num_bins": 50,
        #     "topic": "hist_topic35",
        #     "id": "some_id"
        # }
    ]
}

# CONFIG_JSON = {"cmd": "restart"}

BROKER = 'localhost:9092'
OUTPUT_TOPIC = "from_file"

config = {"bootstrap.servers": BROKER}
producer = Producer(**config)

producer.produce("local_jbi_commands", bytes(json.dumps(CONFIG_JSON), "utf-8"))
producer.flush()
