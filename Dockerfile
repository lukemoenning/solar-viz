# Use the official Python image as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port that Streamlit will run on
EXPOSE 8501

# Set the PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION environment variable
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Run Streamlit when the container launches
CMD ["streamlit", "run", "--server.port", "8501", "SolarViz.py"]