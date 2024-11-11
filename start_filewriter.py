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
                  "module": "dataset",
                  "config": {
                    "name": "title",
                    "values": "This in my title",
                    "type": "string"
                  }
                },
                     {
                         "module": "ev44",
                         "config": {
                             "topic": "local_detector",
                             "source": "grace"
                     }
                        },
                     {
                         "module": "ev44",
                         "config": {
                             "topic": "local_detector",
                             "source": "grace2"
                        }
                     }
                  ]
                }
    ]
}


def generate_config(user, password, brokers, staging):
    return {
        # "security.protocol": "SASL_SSL",
        # "sasl.mechanism": "SCRAM-SHA-256",
        # "ssl.ca.location": "ecdc-kafka-ca-staging.crt"
        # if staging
        # else "ecdc-kafka-ca-real.crt",
        # "sasl.username": user,
        # "sasl.password": password,
        "bootstrap.servers": ",".join(brokers),
    }


def main(kafka_config, pool_topic, inst_topic):
    print(json.dumps(NEXUS_STRUCTURE))
    time_stamp = int(time.time())

    job_id = str(uuid.uuid4())

    print(f"file: {time_stamp}.nxs")
    print(f"job id: {job_id}")

    buffer = serialise_pl72(
        job_id=job_id,
        filename=f"{time_stamp}.nxs",
        start_time=int(time.time()) * 1000,
        # stop_time=(int(time.time())) * 1000,
        run_name="test_run",
        nexus_structure=json.dumps(NEXUS_STRUCTURE),
        service_id=None,
        instrument_name="",
        broker="localhost:9092",
        control_topic=inst_topic,
        metadata="{hello}"
    )

    producer = Producer(**kafka_config)
    producer.produce(pool_topic, buffer)
    producer.flush()

    input("Hit return to close file")
    buffer = serialise_6s4t(
        job_id=job_id,
        run_name="test_run",
        service_id=None,
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

    # required_args.add_argument(
    #     "-u", "--user", type=str, help="the user name", required=True
    # )
    #
    # required_args.add_argument(
    #     "-p", "--password", type=str, help="the password", required=True
    # )

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

    kafka_config = generate_config(None, None, args.brokers, args.staging)

    main(kafka_config, args.pool_topic, args.instrument_topic)
