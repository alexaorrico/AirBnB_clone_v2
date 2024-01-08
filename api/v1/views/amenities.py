#!/usr/bin/python3
""" module view for amenity objects;
handles all default Restful API actions
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.amenity import Amenity
from . import app_views
import uuid


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """gets list of all amenity objects"""
    amenitys = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenitys)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id=None):
    """get amenity by id"""

    # print("Full request: ", request)
    amenity = storage.get(Amenity, amenity_id)
    # print('State id is {}'.format(state_id))
    # print('State id is type {}'.format(type(state_id)))
    # print('State is {}'.format(state))

    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity identified by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """create state from http request"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
