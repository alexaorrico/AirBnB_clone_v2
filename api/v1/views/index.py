#!/usr/bin/python3
"""
import app_views from api.v1.views
create a route/status on the object app_views that returns a JSON: "status": "OK" (see example)
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from flask import jsonify
from flask import Flask


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def return_status():
    """
    returns status
    """
    return jsonify({'status': 'OK'})


@app_views.route('/stats', strict_slashes=False, methods=['GET'])
def stats():
    """
    creates an endpoint that retrieves the
    number of each objects by type
    """
    dic_stats = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(dic_stats)
