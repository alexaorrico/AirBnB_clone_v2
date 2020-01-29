#!/usr/bin/python3
# API routes

from api.v1.views import app_views
from flask import Flask, jsonify
import models

app = Flask(__name__)


@app_views.route('/status')
def status():
    """status ok"""
    return jsonify({
        "status": "OK"
    })


@app_views.route('/stats')
def stats():
    """stats of the resources"""
    return jsonify({
        "amenities": models.storage.count('Amenity'),
        "cities": models.storage.count('City'),
        "places": models.storage.count('Place'),
        "reviews": models.storage.count('Review'),
        "states": models.storage.count('State'),
        "users": models.storage.count('User')
    })
