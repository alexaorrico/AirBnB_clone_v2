#!/usr/bin/python3
""" API view for Amenity objects. """
import os
import json
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('\
/amenities', strict_slashes=False, methods=['GET'])
def all_amenities(text='is_cool'):
    """ Returns list of all Amenity objs. """
    amenities = list(storage.all(Amenity).values())
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('\
/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """ Returns the Amenity obj in JSON. """
    try:
        amenity = storage.all(Amenity)["Amenity.{}".format(amenity_id)]
    except (TypeError, KeyError):
        abort(404)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('\
/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes an Amenity obj from Storage. """
    try:
        amenity = storage.all(Amenity)["Amenity.{}".format(amenity_id)]
    except (TypeError, KeyError):
        abort(404)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('\
/amenities', strict_slashes=False, methods=['POST'])
def create_amenity(text="is_cool"):
    """ Creates a new Amenity and saves to Storage. """
    content = request.get_json()
    try:
        json.dumps(content)
        if 'name' not in content:
            abort(400, {'message': 'Missing name'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    new_amenity = Amenity(**content)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('\
/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates an Amenity obj and saves to Storage. """
    try:
        amenity = storage.all(Amenity)["Amenity.{}".format(amenity_id)]
    except (TypeError, KeyError):
        abort(404)
    if not amenity:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
