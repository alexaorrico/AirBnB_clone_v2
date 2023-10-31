#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

# Mapping of class names to custom identifiers
class_name_map = {
    "users": "User",
    "places": "Place",
    "states": "State",
    "cities": "City",
    "amenities": "Amenity",
    "reviews": "Review"
}

@app_views.route('/status', methods=['GET'])
def status():
    '''Route to return status "OK"'''
    return jsonify({'status': 'OK'})

@app_views.route('/stats', methods=['GET'])
def count():
    '''Retrieves the number of objects by type'''
    object_count = {}
    for endpoint, class_name in class_name_map.items():
        object_count[endpoint] = storage.count(class_name)
    return jsonify(object_count)
