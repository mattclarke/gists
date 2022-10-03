from confluent_kafka import Producer
from streaming_data_types.forwarder_config_update_rf5k import serialise_rf5k, StreamInfo, Protocol
from streaming_data_types.fbschemas.forwarder_config_update_rf5k.UpdateType import (
    UpdateType,
)

CONFIG_TOPIC = "local_forwarder_commands"
BROKER = "localhost:9092"

STREAMS = [
    StreamInfo("IOC:m1.RBV", "f142", "local_motion", Protocol.Protocol.PVA),
    StreamInfo("IOC:m1.VAL", "f142", "local_motion", Protocol.Protocol.PVA),
  ]

config = {"bootstrap.servers": BROKER}
producer = Producer(**config)
producer.produce(CONFIG_TOPIC, serialise_rf5k(UpdateType.ADD, STREAMS))
# producer.send(CONFIG_TOPIC, serialise_rf5k(UpdateType.REMOVEALL, []))

producer.flush()
