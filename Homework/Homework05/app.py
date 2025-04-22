import os
import json
import redis
import requests
from flask import Flask, request, jsonify
from typing import List, Dict, Any

app = Flask(__name__)

# Configure Redis connection from environment variables
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.Redis(host=redis_host, port=redis_port)

@app.route('/meteorites', methods=['POST'])
def load_meteorites() -> Any:
    """
    Fetches meteorite landing data from the public URL and loads it into Redis.
    Returns JSON with load status and count of records.
    """
    url = (
        'https://raw.githubusercontent.com/wjallen/coe332-sample-data/'
        'main/ML_Data_Sample.json'
    )
    response = requests.get(url)
    response.raise_for_status()
    data: List[Dict[str, Any]] = response.json()

    # Store each record as a JSON string in a Redis list
    redis_key = 'meteorites'
    for record in data:
        redis_client.rpush(redis_key, json.dumps(record))

    return jsonify({'status': 'success', 'count': len(data)}), 201

@app.route('/meteorites', methods=['GET'])
def get_meteorites() -> Any:
    """
    Retrieves meteorite landing data from Redis as a JSON list.

    Query Parameters:
      - start (optional): integer index to start from; defaults to 0.

    Returns:
      - List of meteorite records starting at `start`.
      - 400 error if `start` is not an integer.
    """
    start_param = request.args.get('start', None)
    if start_param is not None:
        try:
            start = int(start_param)
        except ValueError:
            return jsonify({'error': 'start must be an integer'}), 400
    else:
        start = 0

    redis_key = 'meteorites'
    raw_items = redis_client.lrange(redis_key, start, -1)
    data = [json.loads(item) for item in raw_items]
    return jsonify(data), 200

if __name__ == '__main__':
    # Listen on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000)
