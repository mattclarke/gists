import random
import time

from confluent_kafka import Producer
from p4p.client.thread import Context
from streaming_data_types import serialise_ev42

OUTPUT_TOPIC = "local_detector"
BROKER = "localhost:9092"
PV = "YMIR-SETS:SE-BADC-001:SLOWDATA"
SCALE = 1_000_000

_CONTEXT = Context('pva', nt=False)

config = {"bootstrap.servers": BROKER}
producer = Producer(**config)

try:
    while True:
        intensity = _CONTEXT.get(PV).value
        tofs = list(range(0, int(intensity * SCALE) + random.randint(0, 10)))
        det_ids = [1] * len(tofs)
        print(f'num events = {len(tofs)}')
        time_ns = time.time_ns()
        buffer = serialise_ev42("laser", time_ns, time_ns, tofs, det_ids)

        producer.produce(OUTPUT_TOPIC, buffer)
        producer.flush()
        time.sleep(0.5)
except:
    pass
