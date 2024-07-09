from kafka import KafkaConsumer
import json
from pathlib import Path
import sys
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))
from src.models.interaction import Interaction
from src.db.interaction_db import InteractionDB
from config.config import KAFKA_BOOTSTRAP_SERVERS,INTERACTIONS_TOPIC


# List of topics to subscribe to
topics = [INTERACTIONS_TOPIC]

# Initialize the consumer
consumer = KafkaConsumer(
    *topics,  # Unpack the list of topics
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',  # Start reading from the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka Consumer Initialized")


# Consume messages from the subscribed topics
for n, message in enumerate(consumer):
    interaction_data = message.value
    print(f"Received message {n + 1} from {INTERACTIONS_TOPIC}: {interaction_data}")

    # Deserialize the message into an Interaction object
    interaction = Interaction.from_dict(interaction_data)

print(f"Processed {n + 1} messages")
