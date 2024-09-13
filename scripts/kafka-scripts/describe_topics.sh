#!/bin/bash

# Describe Kafka topics
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --describe --topic RawNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --describe --topic FilteredNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --describe  --topic ProcessedNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --describe --topic AvailableNewsTopic
/usr/bin/kafka-topics --bootstrap-server localhost:9092 --describe --topic InteractionsTopic
#/usr/bin/kafka-topics --bootstrap-server localhost:9092 --describe --topic __consumer_offsets
