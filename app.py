from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# load env variables
load_dotenv()

app = Flask(__name__)

# Authentication API Key from ENV
API_KEY = os.getenv("API_KEY")


# ------------------------------
# Generate Mock Data (500 rows)
# ------------------------------
def generate_data():

    data = []

    names = ["Alice", "Bob", "Charlie", "David", "Emma"]
    cities = ["New York", "London", "Tokyo", "Berlin", "Paris"]

    base_date = datetime(2024, 1, 1)

    for i in range(1, 501):

        random_days = random.randint(0, 365)
        random_seconds = random.randint(0, 86400)

        date_value = base_date + timedelta(days=random_days)
        timestamp_value = date_value + timedelta(seconds=random_seconds)

        record = {
            "id": i,
            "name": random.choice(names),
            "city": random.choice(cities),
            "created_date": date_value.strftime("%Y-%m-%d"),
            "created_timestamp": timestamp_value.strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(record)

    return data


DATA = generate_data()


# ------------------------------
# Authentication check
# ------------------------------
def check_auth():
    api_key = request.headers.get("x-api-key")
    return api_key == API_KEY


# ------------------------------
# API Endpoint
# ------------------------------
@app.route("/data", methods=["GET"])
def get_data():

    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify(DATA)


# ------------------------------
# Health Check
# ------------------------------
@app.route("/")
def home():
    return jsonify({"message": "Mock API Running"})


# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # needed for Render
    app.run(host="0.0.0.0", port=port)