#!/usr/bin/python3
"""Route to index page"""
from json import dumps
from flask import Response
from api.v1.views import app_views
from models import storage, class_dictionary

classConversion = {"Amenity": "amenities", "City": "cities", "Place": "places",
                   "Review": "reviews", "State": "states", "User": "users"}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Return status of API"""
    return Response(dumps({"status": "OK"}), content_type='application/json')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Return number of objects by type"""
    data = {}
    for cls in class_dictionary.keys():
        data[classConversion[cls]] = storage.count(cls)
    return Response(dumps(data), content_type='application/json')
