# Use python:3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point to run the Flask application
CMD ["python", "app.py"]
