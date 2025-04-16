# Use the official Python 3.9 slim image as the base
FROM python:3.9-slim

# Prevent Python from buffering stdout/stderr so logs appear in real time.
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port that the Flask app runs on (default Flask port is 5000)
EXPOSE 5000

# Set environment variable for Flask
ENV FLASK_APP=app.py

# Start the Flask app
CMD ["python", "app.py"]
