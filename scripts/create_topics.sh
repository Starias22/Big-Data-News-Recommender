#!/bin/bash


# Create Kafka topics with specified retention times
/usr/bin/kafka-topics  --bootstrap-server localhost:9092 --create --topic RawNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=$((2 * 3600 * 1000))   # 2 hours in milliseconds
/usr/bin/kafka-topics  --bootstrap-server localhost:9092 --create --topic FilteredNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=$((2 * 3600 * 1000))   # 2 hours in milliseconds
/usr/bin/kafka-topics  --bootstrap-server localhost:9092 --create --topic ProcessedNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=$((2 * 3600 * 1000))  # 2 hours in milliseconds
/usr/bin/kafka-topics  --bootstrap-server localhost:9092 --create --topic AvailableNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=$((24 * 3600 * 1000))  # 24 hours in milliseconds
/usr/bin/kafka-topics  --bootstrap-server localhost:9092 --create --topic InteractionsTopic --partitions 6 --replication-factor 3 --config retention.ms=$((24 * 3600 * 1000))  # 24 hours in milliseconds

# List Kafka topics

/usr/bin/kafka-topics --list --bootstrap-server localhost:9092
