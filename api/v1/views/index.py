#!/usr/bin/python3
"""This file returns the JSON status ok"""

from flask import Flask, jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import Base, BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenities": Amenity, "Cities": City,
           "Places": Place, "Reviews": Review,
           "States": State, "Users": User}


@app_views.route('/status', strict_slashes=False, methods=['GET'])
def index():
    """home screen of the app"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def num_objects():
    """counts each object in store"""
    result = {}
    for key, value in classes.items():
        total = storage.count(value)
        result[key.lower()] = total
    return jsonify(result)
