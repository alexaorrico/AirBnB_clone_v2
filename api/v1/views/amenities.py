#!/usr/bin/python3
"""
    API module amenities
"""

import models
from models import storage
from models.amenity import *

from flask import jsonify, abort, request
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """
        A function that etrieves the list of all
        Amenity objects: GET /api/v1/amenities
    """
    # get all saved state objects
    objs = storage.all(Amenity).values()

    # Convert state object to dictionary and save in list
    amenityList = [obj.to_dict() for obj in objs]

    return jsonify(amenityList)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
        A function that Retrieves a Amenity
        object: GET /api/v1/amenities/<amenity_id>
    """
    obj = storage.get(Amenity, amenity_id)

    if (obj):
        return jsonify(obj.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """
        A function that Deletes a Amenity object:
        DELETE /api/v1/amenities/<amenity_id>
    """
    obj = storage.get(Amenity, amenity_id)

    # delete and save if state object is found, if not return error 404
    if (obj):
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def add_amenity():
    """
        A function that Creates a Amenity: POST /api/v1/amenities
    """
    # Check If the HTTP body request is not valid JSON
    if (not request.get_json()):
        abort(400, 'Not a JSON')

    json_str = request.get_json()
    if ('name' not in json_str):
        abort(400, 'Missing name')

    # create a new state object, save and return it
    obj = Amenity(**json_str)
    obj.save()

    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
        A function that Updates a Amenity object:
        PUT /api/v1/amenities/<amenity_id>
    """
    obj = storage.get(Amenity, amenity_id)
    if (obj):

        json_str = request.get_json()
        # Check If the HTTP body request is not valid JSON
        if (not json_str):
            abort('400', 'Not a JSON')

        # Update state object attributes
        to_ignore = ['id', 'created_at', 'updated_at']
        for key, value in json_str.items():
            if key not in to_ignore:
                setattr(obj, key, value)

        #  save and return
        obj.save()
        return jsonify(obj.to_dict()), 200
    else:
        abort(404)
