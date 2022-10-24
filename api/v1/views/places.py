#!/usr/bin/python3
"""Routings for amenity-related API requests"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenity_methods():
    """ get all instance of amenity """
    return jsonify({"GET_ALL": "OK"})


@app_views.route('/amenities/<string:id>', methods=['GET'],
                 strict_slashes=False)
def get_single_amenity(id):
    """"get an instance of amenity """
    return jsonify({"GET_ONE": "OK"})


@app_views.route('amenities/<string:id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(id):
    """ delete an instance of amenity """
    return jsonify({"DELETE": "OK"})


@app_views.route('amenities/<string:id>', methods=['POST'],
                 strict_slashes=False)
def add_amenity(id):
    """ create an instance of amenity """
    return jsonify({"POST": "OK"})


@app_views.route('/amenities', methods=['PUT'],
                 strict_slashes=False)
def update_amenity():
    """ update an instance of amenity """
    return jsonify({"PUT": "OK"})
