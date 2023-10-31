#!/usr/bin/python3
"""App index"""
from api.v1.views import app_views
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def index():
    """this returns the api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """counts the number of objs by type"""
    classes = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
            }
    dic_t = {}
    for key, value in classes.items():
        number = storage.count(value)
        dic_t[key] = number
    return jsonify(dic_t)
