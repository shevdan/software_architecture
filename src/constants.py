FACADE = "facade"
LOGGING = "logging"
MESSAGE = "message"
KAFKA = "kafka"

KAFKA_CONFIG_KEY = "msg-q-config"
DEFAULT_KAFKA_CONFIG = {
    "topic": "msg-topic",
    "url": "localhost:9092",
}

HAZELCAST_MAP_KEY = "logging-map-cnf"
DEFAULT_HAZELCAST_MAP_NAME = {"map_name": "logging-map"}