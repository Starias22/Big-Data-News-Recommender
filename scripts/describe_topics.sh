#!/bin/bash

# Describe Kafka topics
/usr/bin/kafka-topics --describe --bootstrap-server localhost:9092 --topic RawNewsTopic
/usr/bin/kafka-topics --describe --bootstrap-server localhost:9092 --topic FilteredNewsTopic
/usr/bin/kafka-topics --describe --bootstrap-server localhost:9092 --topic ProcessedNewsTopic
/usr/bin/kafka-topics --describe --bootstrap-server localhost:9092 --topic AvailableNewsTopic
/usr/bin/kafka-topics --describe --bootstrap-server localhost:9092 --topic InteractionsTopic
