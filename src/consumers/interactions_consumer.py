from kafka import KafkaConsumer
import json
from pathlib import Path
import sys
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))
from profiles.interaction import Interaction
from db.interaction_db import InteractionDB

# Load the configuration from the JSON file
with open('../../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# List of topics to subscribe to
topics = [config["interactions_topic"]]

# Initialize the consumer
consumer = KafkaConsumer(
    *topics,  # Unpack the list of topics
    bootstrap_servers=config["kafka_bootstrap_servers"],
    auto_offset_reset='earliest',  # Start reading from the earliest message
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Kafka Consumer Initialized")

# Initialize MongoDB interaction database
interaction_db = InteractionDB()

print(f"Connected to MongoDB")

# Consume messages from the subscribed topics
for n, message in enumerate(consumer):
    interaction_data = message.value
    print(f"Received message {n + 1}: {interaction_data}")

    # Deserialize the message into an Interaction object
    interaction = Interaction.from_dict(interaction_data)

    # Insert interaction into MongoDB
    result = interaction_db.insert_interaction(interaction)
    print(f"Inserted interaction with ID: {result}")

print(f"Processed {n + 1} messages")