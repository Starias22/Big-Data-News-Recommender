#!/bin/bash

# Delete Kafka topics
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic RawNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic FilteredNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic ProcessedNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic AvailableNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic InteractionsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --delete --topic __consumer_offsets


# List Kafka topics after deletion
/usr/bin/kafka-topics --list --bootstrap-server localhost:9092
