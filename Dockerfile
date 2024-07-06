# Dockerfile

# Use an official Apache Airflow runtime as a parent image
#

# Stage 1: Build Java environment
FROM apache/airflow:2.9.2-python3.11


USER root


# Add the repository line to /etc/apt/sources.list
RUN echo "deb http://deb.debian.org/debian/ sid main" >> /etc/apt/sources.list

RUN apt-get update && apt-get upgrade -y && apt-get install -y apt-transport-https && apt-get install -y openjdk-21-jdk

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64/

RUN export JAVA_HOME


USER airflow




# Copy the current directory contents into the container at /app
# COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install kafka-python newsapi-python GoogleNews apache-airflow-providers-apache-spark nltk pymongo scipy

# Install Streamlit
# RUN pip install streamlit

# Make port 8501 available to the world outside this container
# EXPOSE 8501

# Run Streamlit app.py when the container launches
# CMD ["streamlit", "run", "app.py"]
# CMD ["python3", "src/producers/google_news_producer.py"]

# Copy requirements.txt to the image
#COPY requirements.txt /requirements.txt


#RUN pip install --no-cache-dir -r /requirements.txt


