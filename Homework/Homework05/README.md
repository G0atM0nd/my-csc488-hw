# Homework 05: Flask + Redis Integration

This repository demonstrates a Flask service that loads and retrieves meteorite landing data using a Redis backend.

## Prerequisites
- Docker installed
- An available TCP port for Redis (assigned by ISP)
- Python 3.9+ and pip (for local testing)

## Setup and Usage

1. **Launch Redis container**
   ``bash
   mkdir -p data
   docker run -d \
     --name redis-db \
     -p <ISP_PORT>:6379 \
     -v "$(pwd)/data:/data" \
     redis:6 \
     --save 1 1

Configure and start Flask app (local)

git clone <repo_url>
cd homework05
pip install --user -r requirements.txt
export REDIS_HOST=<REDIS_CONTAINER_IP>
export REDIS_PORT=6379
python app.py

Build and run Flask container
docker build -t <DOCKERHUB_USER>/homework05:latest .
docker run -d \
  --name flask-app \
  --link redis-db \
  -p 5000:5000 \
  -e REDIS_HOST=redis-db \
  <DOCKERHUB_USER>/homework05:latest

Load data: curl -X POST http://localhost:5000/meteorites

Retrieve all: curl http://localhost:5000/meteorites

Retrieve from specific index (10): curl http://localhost:5000/meteorites?start=10

