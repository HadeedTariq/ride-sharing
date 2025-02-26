import os
from dotenv import load_dotenv
from confluent_kafka import Producer, Consumer

# Load environment variables
load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
KAFKA_TOPIC = os.getenv("KAFKA_TOPIC")
KAFKA_GROUP_ID = os.getenv("KAFKA_GROUP_ID")

ssl_config = {
    "bootstrap.servers": KAFKA_BROKER,
    "security.protocol": "SSL",
    "ssl.ca.location": os.getenv("KAFKA_SSL_CA_CERT"),
    "ssl.certificate.location": os.getenv("KAFKA_SSL_CLIENT_CERT"),
    "ssl.key.location": os.getenv("KAFKA_SSL_CLIENT_KEY"),
}

# Kafka Producer
producer = Producer(ssl_config)

# Kafka Consumer
consumer = Consumer(
    {**ssl_config, "group.id": KAFKA_GROUP_ID, "auto.offset.reset": "earliest"}
)
