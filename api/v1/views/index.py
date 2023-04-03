#!/usr/bin/python3
""" index file """

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route('/status')
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats')
def stats():
    """ returns number of objects by type """
    result = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"
               }

    for cls in classes:
        count = storage.count(cls)
        result[classes.get(cls)] = count

    return jsonify(result)
