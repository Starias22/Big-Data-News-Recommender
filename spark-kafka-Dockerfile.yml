
FROM bitnami/spark

# Install curl
USER root
RUN apt-get update && apt-get install -y curl 
#&& rm -rf /var/lib/apt/lists/*

# Install additional Python packages if needed
#RUN pip install numpy nltk

# Download Kafka package for Spark
RUN curl -o /opt/bitnami/spark/jars/spark-sql-kafka-0-10_2.12-3.5.1.jar https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.1/spark-sql-kafka-0-10_2.12-3.5.1.jar

# Copy any necessary files
#COPY requirements.txt /opt/requirements.txt
#RUN pip install -r /opt/requirements.txt

# Ensure necessary environment variables are set
#ENV SPARK_HOME /opt/spark

# Set the entrypoint to Spark
#ENTRYPOINT ["/opt/spark/bin/spark-submit"]
