#!/bin/bash

# Create the main data directory and navigate into it
mkdir data
cd data

# Create directories for Zookeeper
mkdir -p zookeeper/data/ -p zookeeper/log/

# Create directories for Kafka brokers
mkdir -p kafka/log/broker1/ -p kafka/log/broker2/ -p kafka/log/broker3/

# Create directories for checkpoints
mkdir -p checkpoint/filtered_news/ -p checkpoint/available_news/ -p checkpoint/processed_news/

# Create directory for redis, PostgreSQL and MongoDB
mkdir redis/ postgres  mongodb/

# Create directory for Airflow logs
mkdir airflow-logs/

# Navigate back to the parent directory
cd ..


# Set permissions for Zookeeper directories
chmod -R 777 data/checkpoint/{filtered_news,available_news,processed_news}/

# Set permissions for Kafka broker directories
chmod -R 777 data/kafka/log/{broker1,broker2,broker3}/


# Set permissions for checkpoint directories
chmod -R 777 data/checkpoint/{filtered_news,available_news,processed_news}/

# Set permissions for Redis, PostgresQL and MongoDB directories
chmod -R 755 data/{redis,postgres,mongodb}/

# Set permissions for Airflow logs directory
chmod -R 777 data/airflow-logs/