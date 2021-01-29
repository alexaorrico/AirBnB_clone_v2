#!/usr/bin/python3
"""
Module for hbnb API api
"""
from flask import Flask, render_template, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
app = Flask(__name__)


@app_views.route('/status', strict_slashes=False)
def status():
    nominal = {"status": "OK"}
    return jsonify(nominal)


@app_views.route('/stats/', strict_slashes=False)
def stats():
    stats = {"amenities": storage.count('Amenity'),
             "cities": storage.count('City'),
             "places": storage.count('Place'),
             "reviews": storage.count('Review'),
             "states": storage.count('State'),
             "users": storage.count('User')}
    return jsonify(stats)
