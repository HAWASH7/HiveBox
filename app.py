from flask import Flask, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Sensor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)

@app.route('/')
def home():
    return "Welcome to HiveBox API!"

@app.route('/get_data')
def get_sensor_data():
    api_url = "https://api.opensensemap.org/boxes?bbox=8.9,49.9,9.1,50.1"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()  # Get the sensor data
        
        # Save data to the database
        for sensor in data['features']:
            location = sensor['properties'].get('name', 'Unknown Location')
            temperature = sensor['properties'].get('temperature')  # No default value
            humidity = sensor['properties'].get('humidity')  # No default value
            
            new_sensor = Sensor(
                location=location,
                temperature=temperature,
                humidity=humidity
            )
            db.session.add(new_sensor)
        
        db.session.commit()  # Commit all the new sensor entries
        return jsonify(data)  # Return the fetched data as JSON
    else:
        return jsonify({"error": "Failed to fetch data"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database tables if they don't exist
    app.run(debug=True)
