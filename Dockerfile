# Dockerfile

# Use an official Apache Airflow runtime as a parent image
#

# Stage 1: Build Java environment
FROM apache/airflow:2.9.2-python3.10



USER root
RUN apt-get update && apt-get install -y apt-transport-https

RUN apt-get update && apt-get install -y openjdk-21-jdk

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64/
RUN echo $JAVA_HOME
RUN export JAVA_HOME


USER airflow




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
COPY requirements.txt /requirements.txt

# Install the required Python packages as the airflow user
USER airflow
#USER root
RUN pip install --no-cache-dir -r /requirements.txt

#docker build . --tag apache/airflow:2.9.2-python3.10
#docker build . --tag bitnami/spark:latest


#FROM ubuntu
#RUN apt update
#RUN apt install vim #or any package you want
