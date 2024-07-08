FROM python:3.11-slim

# Make port 8501 available to the world outside this container
EXPOSE 8501

#WORKDIR /app

# Install any needed packages 
RUN pip install --upgrade pip
RUN pip install streamlit pymongo kafka-python

# Copy app code and set working directory
#COPY . .

# Run Streamlit app.py when the container launches
#ENTRYPOINT ["streamlit", "run", "app.py"]
