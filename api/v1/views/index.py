#!/usr/bin/python3
"""returns the status of the API"""
from typing import Reversible
import models
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """returns the status of the API"""
    return jsonify(status='OK')

@app_views.route('/stats')
def api_stats():
    """kdnvsj valskd ñd"""
    classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
               "Place": Place, "Review": Review, "State": State, "User": User}
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes[key])
