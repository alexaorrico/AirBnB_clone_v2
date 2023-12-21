#!/usr/bin/python3
"""index module with flask app rutes for status
and stats"""

from api.v1.views import app_views
from flask import jsonify
from models import storage 

@app_views.route('/status')
def status():
    """returns the API status"""
    return jsonify({"status": "OK"})


@app_views.stats('/stats')
def count():
    """use count method to count obj"""
    dict = {}
    clases = {
        "Amenety": amenities,
        "City": cities,
        "Place": places,
        "Review": reviews,
        "State": states,
        "User": users
    }

    for cls, class_list in clases.items():
        counter = storage.count(cls)
        dict[cls] = counter

    return jsonify(dict)
