import configargparse as argparse
from confluent_kafka import Producer
from streaming_data_types.fbschemas.forwarder_config_update_fc00.UpdateType import \
    UpdateType
from streaming_data_types.forwarder_config_update_fc00 import (Protocol,
                                                               StreamInfo,
                                                               serialise_fc00)

STREAMS = [
    StreamInfo(
        "foo:bar:PNPHeartBeatCnt-S",
        "f144",
        "bifrost_motion",
        Protocol.Protocol.PVA,
        1,
    ),
]


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


def main(config, topic):
    producer = Producer(**config)
    producer.produce(topic, serialise_fc00(UpdateType.REMOVEALL, []))
    # producer.produce(topic, serialise_fc00(UpdateType.ADD, STREAMS))
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
