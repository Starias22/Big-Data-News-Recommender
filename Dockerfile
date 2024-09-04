FROM python:3.11-slim 
# Make port 5000 available to the world outside this container
EXPOSE 5000
# Install any needed packages
RUN pip install --upgrade pip
RUN pip install Flask pymongo kafka-python
