#!/usr/bin/python3
"""A host file for status of objects of api blueprint."""

# Importing modules from system files
from flask import jsonify

# Importing modules from my files
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """Function to get status of API"""
    return jsonify(status="OK")


@app_views.route('/stats')
def get_stats():
    """Retrieves numbers of Each objects by type."""
    obj = {
            'amenities': Amenity,
            'cities': City,
            'places': Place,
            'reviews': Review,
            'states': State,
            'users': User
            }
    for key, value in obj.items():
        obj[key] = storage.count(value)

    return jsonify(obj)
