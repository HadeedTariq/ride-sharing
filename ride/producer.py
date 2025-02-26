from .kafka_config import producer, KAFKA_TOPIC


def send_message(message):
    producer.produce(KAFKA_TOPIC, value=message)
    producer.flush()
    print("Message sent!")
