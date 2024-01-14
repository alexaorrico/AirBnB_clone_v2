#!/usr/bin/python3
"""
Flask route on the object app_views that returns json status response
"""
import sys

sys.path.append('/AirBnB_clone_v3/api/v1')

from views import app_views

sys.path.append('/AirBnB_clone_v3')

import models
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify, request


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns status
    """
    return jsonify({"status": "OK"})

def api_stats():
    """checks the API status of all classes"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
