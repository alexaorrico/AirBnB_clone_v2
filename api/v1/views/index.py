#!/usr/bin/python3
<<<<<<< HEAD
"""index - end point"""
=======
"""This returns all the classes."""
>>>>>>> 2f785afc83268335f06aedd42646c8c0ff3ef96d
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "OK"})


<<<<<<< HEAD
@app_views.route("/stats")
def opbjects():
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
=======
@app_views.route('/stats', methods=['GET'])
def stats():
    return jsonify({
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
>>>>>>> 2f785afc83268335f06aedd42646c8c0ff3ef96d
    })
