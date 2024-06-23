#!/bin/bash

KAFKA_BIN_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/bin/
KAFKA_CONFIG_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/config/
KAFKA_LOGS_PATH=~/Big-Data-News-Recommender/kafka-3.7.0-src/kafka-logs/

# Remove meta.properties files
rm -f ${KAFKA_LOGS_PATH}broker*/meta.properties

# Stop Kafka Servers
nohup ${KAFKA_BIN_PATH}kafka-server-stop.sh ${KAFKA_CONFIG_PATH}kafka-server1.properties > output/servers/server1.log 2>&1 &
nohup ${KAFKA_BIN_PATH}kafka-server-stop.sh ${KAFKA_CONFIG_PATH}kafka-server2.properties > output/servers/server2.log 2>&1 &
nohup ${KAFKA_BIN_PATH}kafka-server-stop.sh ${KAFKA_CONFIG_PATH}kafka-server3.properties > output/servers/server3.log 2>&1 &


# Stop Zookeeper
nohup ${KAFKA_BIN_PATH}zookeeper-server-stop.sh ${KAFKA_CONFIG_PATH}zookeeper.properties > output/zookeeper.log 2>&1 &


