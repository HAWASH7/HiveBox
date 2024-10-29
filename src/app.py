# src/app.py

from flask import Flask, jsonify
from datetime import datetime, timedelta
import random

app = Flask(__name__)

# Define the app version
app_version = 'v0.0.1'

# Mock data for senseBox (for example purposes)
senseBox_data = [
    {'temperature': random.uniform(15.0, 30.0), 'timestamp': datetime.now() - timedelta(minutes=random.randint(0, 59))}
    for _ in range(10)  # Simulating 10 readings
]

@app.route('/version', methods=['GET'])
def version():
    return jsonify({'version': app_version})

@app.route('/temperature', methods=['GET'])
def temperature():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    recent_readings = [data['temperature'] for data in senseBox_data if data['timestamp'] >= one_hour_ago]

    if not recent_readings:
        return jsonify({'error': 'No recent temperature data available.'}), 404

    average_temp = sum(recent_readings) / len(recent_readings)
    return jsonify({'average_temperature': average_temp})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
