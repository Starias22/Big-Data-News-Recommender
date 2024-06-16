import json
from kafka import KafkaProducer

from pathlib import Path
import sys

# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[1]
sys.path.append(str(src_path))

from profiles.interaction import Interaction

# Load configuration
with open('../../config/config.json', 'r') as config_file:
    config = json.load(config_file)
# Define the Kafka producer
class InteractionProducer:
    def __init__(self, kafka_server=config['kafka_bootstrap_servers'], 
                 topic=config["interactions_topic"]):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.topic = topic

    def send_interaction(self, interaction):
        interaction_dict = interaction.to_dict()
        self.producer.send(self.topic, interaction_dict)
        self.producer.flush()
        print(f"Sent interaction: {interaction_dict}")

# Example usage
if __name__ == "__main__":
    # Create an Interaction instance
    interaction_instance = Interaction(
        sentiment=0.926,
        news_id='google_news_225',
        user_id='666d7c7cc2c9c814c5597193',
        features={'type': 0, 'size': 73567, 'indices': [11, 13, 23, 24, 324, 654, 724, 727, 730, 909, 1032, 1390, 1433, 1964, 3916, 5547, 5592, 12406, 69077], 'values': [3.950578384983817, 4.137702008380003, 4.296066814412818, 4.357292996293112, 5.697170676385995, 6.186810280148589, 6.24551129294779, 6.247014487518703, 6.260645898894849, 6.459961982119212, 6.579433273161303, 6.814180330193821, 6.851334215191439, 7.146153419355295, 7.961019281350807, 8.315608718798519, 8.324577388781279, 9.450588651637503, 12.746425517641832]},  

        topicDistribution={'type': 1, 'values': [0.00028431585261334016, 0.0002853380197610555, 0.0002833482118958136, 0.00028218864234672166, 0.00028517320259443976, 0.06342009325259852, 0.00028415743067454984, 0.20088136735196108, 0.2671208134981876, 0.00028199495430623455, 0.0755324339301018, 0.000282749852072471, 0.00028346399199452685, 0.0002844599210754444, 0.00028280938218729193, 0.0002798591029204592, 0.07337048610467094, 0.04627353335503064, 0.18338551945213533, 0.08379373601060229, 0.0002803862955392675, 0.0002834289768920505, 0.0002823445628326572, 0.0002822661786758182, 0.00028104933513845964, 0.00028205470127983754, 0.0002824385973456839, 0.00028268379856187054, 0.000282855341943268, 0.00028265069206050755]},
        category=1
    )
    # Initialize the InteractionProducer
    interaction_producer = InteractionProducer()

    # Send the interaction
    interaction_producer.send_interaction(interaction_instance)
