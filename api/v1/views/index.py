#!/usr/bin/python3
"""api index"""
from api.v1.views import app_views
from flask import Response
from json import dumps
from models import storage, classes

cc = {"Amenity": "amenities", "City": "cities", "Place": "places",
      "Review": "reviews", "State": "states", "User": "users"}


@app_views.route('/status',  methods=['GET'], strict_slashes=False)
def status():
    """returns the status of the API"""
    return Response(dumps({"status": "OK"}), content_type='application/json')


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """returns the stats"""
    data = {}
    for cls in classes.keys():
        data[cc[cls]] = storage.count(cls)
    return Response(dumps(data), content_type='application/json')
