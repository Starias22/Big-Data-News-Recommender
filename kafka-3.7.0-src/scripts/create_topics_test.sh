#!/bin/bash

# Define Kafka binaries and configurations path
KAFKA_BIN_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/bin/
KAFKA_CONFIG_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/config/
KAFKA_LOGS_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/kafka-logs/

# Create Kafka topics
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --create --topic RawNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=1800000 # 30 minutes in milliseconds
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --create --topic FilteredNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=1800000 # 30 minutes in milliseconds
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --create --topic ProcessedNewsTopic --partitions 6 --replication-factor 3 --config retention.ms=3600000 # 1 hour in milliseconds
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --create --topic InteractionsTopic --partitions 6 --replication-factor 3 --config retention.ms=3600000 # 1 hour in milliseconds

# List Kafka topics
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --list
