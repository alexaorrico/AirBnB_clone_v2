#!/usr/bin/python3

"""
Creating a blueprint with the URL prefix
"""

from flask import Blueprint, jsonify
from models import storage
from models.state import State
from models.city import City


# Create a blueprint with the URL
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


# Define route
@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns a JSON response indicating the status is OK."""
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'])
def get_stats():
    """Retrieve the number of objects by type"""
    counts = {
        'State': storage.count(State),
        'City': storage.count(City),
    }

    return jsonify(counts)
