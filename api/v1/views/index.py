#!/usr/bin/python3
"""API Stats"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Get the count of each object type"""
    count_dict = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
