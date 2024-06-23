#!/bin/bash

# Define Kafka binaries path
KAFKA_BIN_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/bin/

# Describe Kafka topics
${KAFKA_BIN_PATH}kafka-topics.sh --bootstrap-server localhost:9092 --describe 
