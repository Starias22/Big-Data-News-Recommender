from kafka import KafkaConsumer
import json
import sys
from pathlib import Path


    
# Add 'src' directory to the Python path
src_path = Path(__file__).resolve().parents[2]
sys.path.append(str(src_path))

from config.config import KAFKA_BOOTSTRAP_SERVERS, RAW_NEWS_TOPIC

# List of topics to subscribe to
topics = [RAW_NEWS_TOPIC]
          #, 'topic2'
          

# Initialize the consumer
consumer = KafkaConsumer(
    *topics,  # Unpack the list of topics
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest', # Retrieve all the mesage published to the topic and still available
    #auto_offset_reset='latest', # Retrieve all the meaage published since the consumer started
    #auto_offset_reset='none', # 
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    
)

print(consumer)


n=0


# Consume messages from the subscribed topics
for message in consumer:
    print(f"Received message from topic {message.topic}: {message.value}")
    n+=1
    print(n)

#print(len(consumer))
