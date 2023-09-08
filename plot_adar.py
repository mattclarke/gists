import time
import configargparse as argparse

import matplotlib.pyplot as plt
import numpy as np
from confluent_kafka import Consumer, TopicPartition
from streaming_data_types import deserialise_ADAr


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
        "group.id": f"consumer-{time.time_ns()}",
        "auto.offset.reset": "latest",
    }


def _get_metadata_blocking(consumer):
    while True:
        try:
            return consumer.list_topics(timeout=1)
        except Exception:
            print("Cannot get topic metadata - broker(s) down?")
            time.sleep(0.1)


def main(kafka_config, topic):
    consumer = Consumer(kafka_config)

    metadata = _get_metadata_blocking(consumer)
    if topic not in metadata.topics:
        raise Exception("Topic does not exist")

    topic_partitions = [
        TopicPartition(topic, p) for p in metadata.topics[topic].partitions
    ]

    consumer.assign(topic_partitions)

    while (msg := consumer.poll(timeout=0.5)) is None:
        time.sleep(0.1)

    result = deserialise_ADAr(msg.value())

    fig = plt.figure(1)
    x, y = np.meshgrid(list(range(result.data.shape[0] + 1)), list(range(result.data.shape[1] + 1)))
    ax = fig.add_subplot(111)
    ax.pcolormesh(x, y, result.data.T)
    plt.show()


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
        "-t", "--topic", type=str, help="the config topic", required=True
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

    main(kafka_config, args.topic)
