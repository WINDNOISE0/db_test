def send_event(producer, topic, message):
    producer.send(topic, value=message)
    producer.flush()
