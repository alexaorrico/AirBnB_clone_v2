#!/usr/bin/python3
"""returns the status of the API"""
import models
from models import storage
from models.base_model import BaseModel
from models.state import State
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def api_status():
    """returns the status of the API"""
    return jsonify(status='OK')

@app_views.route('/stats')
def api_stats():
    """checks the API stats of all classes"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    for key in classes:
        classes[key] = storage.count(classes[key])
    return jsonify(classes)
