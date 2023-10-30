#!/usr/bin/python3
'''API status'''
from models import storage
from models.state import State
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    '''Returns the API status.'''
    return jsonify(status="OK")

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    '''Returns the count of each type of object.'''
    classes = {
        "states": State,
        "users": User,
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review
    }
    stats = {key: storage.count(value) for key, value in classes.items()}
    return jsonify(stats)
