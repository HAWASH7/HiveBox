from flask import Flask, jsonify
import redis
import boto3
import time
import threading

app = Flask(__name__)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

minio_client = boto3.client(
    's3',
    endpoint_url='http://localhost:9000',  
    aws_secret_access_key='minioadmin'
)

SENSEBOXES = [...]
STORE_INTERVAL = 300 
last_cached_time = time.time()

def store_data():
    while True:
        print("Storing data in MinIO...")
        time.sleep(STORE_INTERVAL)

@app.route('/store', methods=['POST'])
def store():
    print("Storing data immediately in MinIO...")
    return jsonify({"message": "Data stored"}), 200

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify({"custom_metrics": "..."})  

@app.route('/readyz', methods=['GET'])
def readyz():
    global last_cached_time
    sensebox_failures = sum(1 for box in SENSEBOXES if not is_sensebox_accessible(box))
    
    if (time.time() - last_cached_time > 300) and (sensebox_failures > len(SENSEBOXES) / 2):
        return jsonify({"status": "unhealthy"}), 503

    return jsonify({"status": "healthy"}), 200

def is_sensebox_accessible(box):
    return True

if __name__ == '__main__':
    threading.Thread(target=store_data, daemon=True).start()  
    app.run(debug=True)
