# src/app.py

from flask import Flask, jsonify
from datetime import datetime, timedelta
import random
import os
from prometheus_client import generate_latest, CollectorRegistry, Gauge

app = Flask(__name__)

app_version = 'v0.0.1'

senseBox_data = [
    {'temperature': random.uniform(15.0, 30.0), 'timestamp': datetime.now() - timedelta(minutes=random.randint(0, 59))}
    for _ in range(10) 

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


SENSEBOX_TEMP = os.getenv("SENSEBOX_TEMP", "20")  

registry = CollectorRegistry()
temperature_gauge = Gauge('average_temperature', 'Average temperature from senseBox', registry=registry)

@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest(registry), 200

@app.route('/temperature', methods=['GET'])
def temperature():
    try:
        avg_temp = float(SENSEBOX_TEMP)
    except ValueError:
        return jsonify({"error": "Invalid temperature value"}), 400

    if avg_temp < 10:
        status = "Too Cold"
    elif 11 <= avg_temp <= 36:
        status = "Good"
    else:
        status = "Too Hot"

    return jsonify({"average_temperature": avg_temp, "status": status}), 200
