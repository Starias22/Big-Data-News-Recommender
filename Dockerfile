FROM python:3.11-slim 
# Make port 8501 available to the world outside this container
EXPOSE 8501
# Install any needed packages 
RUN pip install --upgrade pip
RUN pip install streamlit pymongo kafka-python
