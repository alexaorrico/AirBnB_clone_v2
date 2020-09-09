#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 14:42:23 2020
@authors: Robinson Montes.
          Mauricio Olarte
"""
from flask import jsonify, Blueprint
from . import app_views
from models import storage

index_view = Blueprint('index_view', __name__,
                       template_folder='views', url_prefix='/api/v1/')

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ check the status of route """
    return jsonify({'status': 'OK'})


@index_view.route('/stats', methods=['GET'], strict_slashes=False)
def object_status():
    """Create an endpoint that retrieves the number of each objects by type
    """
    objects = {"amenities": 'Amenity', "cities": 'City', "places": 'Place',
               "reviews": 'Review', "states": 'State', "users": 'User'}
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
