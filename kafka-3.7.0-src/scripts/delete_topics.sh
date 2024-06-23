#!/bin/bash

# Define Kafka binaries and configurations path
KAFKA_BIN_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/bin/
KAFKA_CONFIG_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/config/
KAFKA_LOGS_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/kafka-logs/


# Delete Kafka topics
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic RawNewsTopic
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic FilteredNewsTopic
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic ProcessedNewsTopic
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic InteractionsTopic

# List Kafka topics
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --list
