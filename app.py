from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to HiveBox API!"

@app.route('/get_data')
def get_sensor_data():
    api_url = "https://api.opensensemap.org/boxes?bbox=8.9,49.9,9.1,50.1"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()  # Get the sensor data
        return jsonify(data)     # Return as JSON
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
