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
from config.config import KAFKA_BOOTSTRAP_SERVERS,INTERACTIONS_TOPIC,TIME_OUT_MS


# Initialize the consumer
consumer = KafkaConsumer(
    INTERACTIONS_TOPIC, 
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',  # Start reading from the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
)

print("Kafka Consumer Initialized")

n=0
# Consume messages from the subscribed topics
for message in consumer:
    interaction_data = message.value
    print(f"Received message {n + 1} from {INTERACTIONS_TOPIC}: {interaction_data}")

    # Deserialize the message into an Interaction object
    interaction = Interaction.from_dict(interaction_data)
    n+=1

print(f"Processed {n} messages")
