#!/usr/bin/python3
"""
Defines index views for the AirBnB clone v3 API.
Includes endpoints for checking the status of the API and
retrieving the number of objects by type.
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def get_status():
    """
    Returns the current status of the API.
    """
    return jsonify(status='OK')


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """
    Returns the count of each object type in storage.
    """
    classes = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }
    counts = {cls_name: storage.count(cls)
              for cls_name, cls in classes.items()}
    return jsonify(counts)
