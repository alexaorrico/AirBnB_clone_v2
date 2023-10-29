#!/usr/bin/python3
"""Status of the api"""

import models
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.base_model import BaseModel


@app_views.route('/status', strict_slashes=False)
def returnstuff():
    '''return stuff'''
    return jsonify(status='OK')


@app_views.route('/stats', strict_slashes=False)
def statistics():
    '''Method that returns the statistics
    about various stuff in JSON format'''
    todo = {'states': State, 'users': User,
            'amenities': Amenity, 'cities': City,
            'places': Place, 'reviews': Review}
    for key in todo:
        todo[key] = storage.count(todo[key])
    return jsonify(todo)
