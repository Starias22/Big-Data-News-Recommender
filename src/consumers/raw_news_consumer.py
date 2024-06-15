from kafka import KafkaConsumer
import json

# Load the configuration from the JSON file
with open('../../config/config.json', 'r') as config_file:
    config = json.load(config_file)

# List of topics to subscribe to
topics = [config["raw_news_topic"]
          #, 'topic2'
          ]

# Initialize the consumer
consumer = KafkaConsumer(
    *topics,  # Unpack the list of topics
    bootstrap_servers=config["kafka_bootstrap_servers"],
    auto_offset_reset='earliest', # Retrieve all the mesage published to the topic and still available
    #auto_offset_reset='latest', # Retrieve all the meaage published since the consumer started
    #auto_offset_reset='none', # 
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    #group_id='my-group'
)

print(consumer)


n=0


# Consume messages from the subscribed topics
for message in consumer:
    print(f"Received message from topic {message.topic}: {message.value}")
    n+=1
    print(n)

#print(len(consumer))
