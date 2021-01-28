"""Status APi """
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """Status API by json file"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_obj():
    """ Count the objects in each class"""
    return jsonify({"amenities": storage.count('Amenity'),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
