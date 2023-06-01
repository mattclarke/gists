import json

from confluent_kafka import Producer


HEIGHT = 10
WIDTH = 10
BROKER = 'localhost:9092'
OUTPUT_TOPIC = "local_detector"


config = {"bootstrap.servers": BROKER}
producer = Producer(**config)


CONFIG_JSON = {
    "cmd": "config",
    "interval": 10,
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
        }
    ]
}

producer.produce("local_jbi_commands", bytes(json.dumps(CONFIG_JSON), "utf-8"))
producer.flush()
