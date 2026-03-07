from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# ------------------------------
# Load Environment Variables
# ------------------------------
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


# ------------------------------
# Authentication Middleware
# ------------------------------
@app.before_request
def authenticate():

    # Allow health check endpoint
    if request.path == "/":
        return None

    api_key = request.headers.get("x-api-key")

    if api_key != API_KEY:
        return jsonify({
            "status": "failed",
            "message": "Unauthorized - Invalid API Key"
        }), 401


# ------------------------------
# Generate Mock Data
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
# Data API with Pagination + Date Filter
# ------------------------------
@app.route("/data", methods=["GET"])
def get_data():

    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 50))

    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    filtered_data = DATA

    # Date Filtering
    if start_date:
        filtered_data = [
            r for r in filtered_data
            if r["created_date"] >= start_date
        ]

    if end_date:
        filtered_data = [
            r for r in filtered_data
            if r["created_date"] <= end_date
        ]

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    paginated_data = filtered_data[start:end]

    return jsonify({
        "page": page,
        "limit": limit,
        "total_records": len(filtered_data),
        "data": paginated_data
    })


# ------------------------------
# Health Check Endpoint
# ------------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Mock API Running",
        "status": "healthy"
    })


# ------------------------------
# Run App (Required for Render)
# ------------------------------
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )
