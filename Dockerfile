# Dockerfile

# Use an official Apache Airflow runtime as a parent image
#

# Stage 1: Build Java environment
FROM apache/airflow:2.9.2-python3.10



USER root

RUN apt-get update -y

# Copy Java environment from the java_base stage
#COPY --from=java_base /usr/lib/jvm/java-11-openjdk /usr/lib/jvm/java-11-openjdk

# Optionally, set Java environment variables
#ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk
#ENV PATH="$PATH:$JAVA_HOME/bin"

USER airflow


#FROM apache/airflow:2.9.2-python3.10

#USER root



#RUN apt install 



#FROM python:3.10-slim-buster
#FROM java:7
#FROM apache/spark-py
#FROM bitnami/spark:latest
#FROM debian:bullseye

# Update package lists and install necessary packages

# Set the working directory in the container
# WORKDIR /app

# Install Java (OpenJDK) and set JAVA_HOME
#USER root
#RUN apt-get update && apt-get install -y openjdk-11-jdk
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

#USER root

# Install OpenJDK-11


#RUN apt update --allow-insecure-repositories
# docker image prune -a
# Set JAVA_HOME
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
#RUN export JAVA_HOME

# Set JAVA_HOME
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
#RUN export JAVA_HOME

# Install Java 11 JDK
#RUN apt-get update && \
    #apt-get install -y --no-install-recommends gnupg2 ca-certificates openjdk-11-jdk && \
    #rm -rf /var/lib/apt/lists/*
# Set JAVA_HOME environment variable
#ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

# Copy the current directory contents into the container at /app
# COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --upgrade pip
# RUN pip install kafka-python-ng
# RUN pip install newsapi-python
# RUN pip install --no-cache-dir -r requirements.txt

# Install Streamlit
# RUN pip install streamlit

# Make port 8501 available to the world outside this container
# EXPOSE 8501

# Run Streamlit app.py when the container launches
# CMD ["streamlit", "run", "app.py"]
# CMD ["python3", "src/producers/google_news_producer.py"]

# Copy requirements.txt to the image
#COPY requirements.txt /requirements.txt

# Install the required Python packages as the airflow user
USER airflow
#USER root
RUN pip install --no-cache-dir -r /requirements.txt

#docker build . --tag apache/airflow:2.9.2-python3.10
#docker build . --tag bitnami/spark:latest


#FROM ubuntu
#RUN apt update
#RUN apt install vim #or any package you want