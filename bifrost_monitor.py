import random
import threading
import time

import numpy as np

from confluent_kafka import Producer
from p4p.nt import NTScalar
from p4p.server import Server
from p4p.server.thread import SharedPV
from streaming_data_types import serialise_ev42

OUTPUT_TOPIC = "ymir_detector"
BROKER = "10.100.1.19:9092"
PV = "BIFROST:MON_MODE"
mode = 0


def send_events():
    global mode
    config = {"bootstrap.servers": BROKER}
    producer = Producer(**config)
    while True:
        if mode == 0:
            # Single pixel mode
            tofs = [int(x) for x in np.random.normal(5000, 1000, 1000)]
            dets = [1] * len(tofs)
        else:
            tofs = [int(x) for x in np.random.normal(5000, 1000, 1000)]
            dets = [random.randint(1, 101) for _ in range(len(tofs))]

        time_ns = time.time_ns()
        buffer = serialise_ev42("bifrost_mon", time_ns, time_ns, tofs, dets)
        producer.produce(OUTPUT_TOPIC, buffer)
        producer.flush()
        time.sleep(1)


thread = threading.Thread(target=send_events, daemon=True)
thread.start()

pv = SharedPV(nt=NTScalar('d'), initial=0.0)


@pv.put
def handle(pv, op):
    global mode
    pv.post(op.value())
    if op.value() > 0:
        print('switching to position sensitive mode')
        mode = 1
    else:
        print('switching to single pixel mode')
        mode = 0
    op.done()


Server.forever(providers=[{PV: pv}])
