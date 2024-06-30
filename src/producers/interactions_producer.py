import json
from kafka import KafkaProducer
from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from src.models.interaction import Interaction
from config.config import KAFKA_BOOTSTRAP_SERVERS, INTERACTIONS_TOPIC,LIKED


def send_interaction(interaction):
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    
    interaction_dict = interaction.to_dict()
    producer.send(INTERACTIONS_TOPIC, interaction_dict)
    producer.flush()
    print(f"Sent interaction: {interaction_dict}")


# Example usage
if __name__ == "__main__":
    # Create an Interaction instance
    interaction_instance = Interaction(
        news_id='google_news_225',
        user_id='666d7c7cc2c9c814c5597193',
        features=2222,
        action=LIKED
    )
    
    # Send the interaction
    send_interaction(interaction_instance)
