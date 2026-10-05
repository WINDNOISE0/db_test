from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


def create_topic(topic_name, num_partitions=1, replication_factor=1,
                 bootstrap_servers="localhost:9092"):
    admin = KafkaAdminClient(bootstrap_servers=bootstrap_servers)
    try:
        admin.create_topics([
            NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
            )
        ])
    except TopicAlreadyExistsError:
        # Идемпотентность: повторный прогон теста не должен падать
        pass
    finally:
        admin.close()