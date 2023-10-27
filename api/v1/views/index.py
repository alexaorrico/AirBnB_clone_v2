#!/usr/bin/python3
"""
API Index View Module

Defines the API views for the status endpoint, by creating a route /status on
the object app_views that returns a JSON: 'status': 'OK'.
"""

from flask import jsonify
from api.v1.views import app_views
import models
from models import storage
from models.base_model import BaseModel


@app_views.route('/status', strict_slashes=False)
def get_status():
    """ Returns the status of the API in JSON format """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_objs_type():
    """ Retrieves the number of each objects by type """
    objs = {'states': State,
            'cities': City,
            'users': User,
            'places': Place,
            'amenities': Amenity,
            'reviews': Review}

    for k in objs:
        objs[k] = storage.count(objs[k])
    return jsonify(objs)
