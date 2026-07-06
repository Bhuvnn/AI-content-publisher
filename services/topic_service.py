import yaml
import random
from datetime import datetime
from app.config import COOLDOWN_DAYS,YAML_PATH

def load_topics_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def choose_topic(topic_data):
    topics = topic_data["topics"]
    if not topics:
        raise ValueError("No topics found in topics.yaml")

    unused_topics = []
    eligible_topics = []

    for topic in topics:

        # Never used before
        if topic["last_used"] is None:
            unused_topics.append(topic)
            continue

        # Convert string to datetime
        last_used = datetime.fromisoformat(topic["last_used"])

        days_since_last_use = (datetime.now() - last_used).days

        if days_since_last_use >= COOLDOWN_DAYS:
            eligible_topics.append(topic)

    # Prefer topics that have never been used
    if unused_topics:
        topic=random.choice(unused_topics)
        return topic["name"]

    # Otherwise choose from eligible topics
    if eligible_topics:
        topic=random.choice(eligible_topics)
        return topic["name"]

    # If everything is on cooldown, choose any topic
    topic=random.choice(topics)
    return topic["name"]


def get_next_topic():
    topics=load_topics_from_yaml(YAML_PATH)
    return choose_topic(topics)
