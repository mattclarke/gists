import json
import time
import uuid

from kafka import KafkaProducer
from streaming_data_types.run_start_pl72 import serialise_pl72
from streaming_data_types.run_stop_6s4t import serialise_6s4t

CONFIG_TOPIC = "local_filewriter_pool"
nexus = {
    "children": [
        {
            "type": "group",
            "name": "entry",
            "children": [
                {
                    "type": "group",
                    "name": "events",
                    "children": [
                        {
                            "type": "stream",
                            "stream": {
                                "topic": "TEST_nicosCacheCompacted",
                                "source": "not_nicos/fake/value",
                                "writer_module": "ns10",
                            },
                        }
                    ],
                    "attributes": [{"name": "NX_class", "values": "NXgroup"}],
                }
            ],
        }
    ]
}

time_stamp = int(time.time())

job_id = str(uuid.uuid4())

print(f"file: {time_stamp}.nxs")
print(f"job id: {job_id}")

buffer = serialise_pl72(
    job_id=job_id,
    filename=f"{time_stamp}.nxs",
    # start_time = 1547198055000,
    # stop_time = 1647198055000,
    run_name="test_run",
    nexus_structure=json.dumps(nexus),
    service_id="",
    instrument_name="TEST",
    broker="localhost:9092",
    control_topic="local_filewriter",
)

producer = KafkaProducer(bootstrap_servers="localhost:9092")
producer.send(CONFIG_TOPIC, buffer)
producer.flush()

input("Hit return to close file")
buffer = serialise_6s4t(
    job_id=job_id,
    run_name="test_run",
    service_id="",
    stop_time=None,
    command_id=str(uuid.uuid4()),
)

producer.send("local_filewriter", buffer)
producer.flush()
