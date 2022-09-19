#!/usr/bin/python
"""
server configuration
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """return succsess code 200"""

    json = {
        "status": "OK"
    }
    return jsonify(json)


@app_views.route('/stats')
def stats():
    """return each class how much object instance"""

    obj_instance = {"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")}
    return jsonify(obj_instance)
