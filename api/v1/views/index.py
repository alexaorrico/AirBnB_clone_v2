#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from flask import request, jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ return JSON response OK """
    if request.method == 'GET':
        return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ retrives the number of each objects by type """
    print('hello!')
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    objects_stats = {}
    objects_stats["amenities"] = storage.count(Amenity)
    objects_stats["cities"] = storage.count(City)
    objects_stats["places"] = storage.count(Place)
    objects_stats["reviews"] = storage.count(Review)
    objects_stats["states"] = storage.count(State)
    objects_stats["users"] = storage.count(User)
    return jsonify(objects_stats)
