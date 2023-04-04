#!/usr/bin/python3
"""API routes for status and stats endpoints."""
import os
from flask import Flask, jsonify
from flask_cors import CORS
from api.v1.views import app_views
from models import storage

from flask import Flask, jsonify
from models import storage

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_status():
    """Returns status of API."""
    return jsonify({"status": "OK"})

@app.route('/stats', methods=['GET'])
def get_stats():
    """Returns count of each type of object in database."""
    count_stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(count_stats)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)