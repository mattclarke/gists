import json
import time
import uuid

import configargparse as argparse
from confluent_kafka import Producer
from streaming_data_types.run_start_pl72 import serialise_pl72
from streaming_data_types.run_stop_6s4t import serialise_6s4t


NEXUS_STRUCTURE = {
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


def generate_config(user, password, brokers, staging):
    return {
        "security.protocol": "SASL_SSL",
        "sasl.mechanism": "SCRAM-SHA-256",
        "ssl.ca.location": "ecdc-kafka-ca-staging.crt"
        if staging
        else "ecdc-kafka-ca-real.crt",
        "sasl.username": user,
        "sasl.password": password,
        "bootstrap.servers": ",".join(brokers),
        "message.max.bytes": 1_000_000_000,
    }


def main(kafka_config, pool_topic, inst_topic):
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
        nexus_structure=json.dumps(NEXUS_STRUCTURE),
        service_id="",
        instrument_name="TEST",
        broker="localhost:9092",
        control_topic=inst_topic,
    )

    producer = Producer(**kafka_config)
    producer.produce(pool_topic, buffer)
    producer.flush()

    input("Hit return to close file")
    buffer = serialise_6s4t(
        job_id=job_id,
        run_name="test_run",
        service_id="",
        stop_time=None,
        command_id=str(uuid.uuid4()),
    )

    producer.produce(inst_topic, buffer)
    producer.flush()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument(
        "-b",
        "--brokers",
        type=str,
        nargs="+",
        help="the broker addresses",
        required=True,
    )

    required_args.add_argument(
        "-pt", "--pool-topic", type=str, help="the pool topic", required=True
    )

    required_args.add_argument(
        "-it",
        "--instrument-topic",
        type=str,
        help="the instrument topic",
        required=True,
    )

    required_args.add_argument(
        "-u", "--user", type=str, help="the user name", required=True
    )

    required_args.add_argument(
        "-p", "--password", type=str, help="the password", required=True
    )

    parser.add_argument(
        "-c",
        "--config-file",
        is_config_file=True,
        help="configuration file",
    )

    parser.add_argument(
        "-s",
        "--staging",
        type=bool,
        default=False,
        help="Is it the staging environment?",
    )

    args = parser.parse_args()

    kafka_config = generate_config(args.user, args.password, args.brokers, args.staging)

    main(kafka_config, args.pool_topic, args.instrument_topic)
