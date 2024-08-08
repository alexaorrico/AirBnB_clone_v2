#!/usr/bin/python3
"""
Module defines view for Amenity objects that handles all default
RESTFUL API actions.
"""
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """ Retrieves all Amenity objects """
    amenity_objs = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenity_objs]

    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieves Amenity object by amenity_id """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    return jsonify(amenity_obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes Amenity object by amenity_id """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    storage.delete(amenity_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates Amenity object """
    try:
        data = request.get_json()
        if 'name' not in data:
            abort(400, description='Missing name')
    except BadRequest:
        abort(400, description='Not a JSON')

    amenity_obj = Amenity(**data)
    storage.new(amenity_obj)
    storage.save()

    return jsonify(amenity_obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates Amenity object by amenity_id """
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    try:
        data = request.get_json()
    except BadRequest:
        abort(400, description='Not a JSON')

    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity_obj, key, value)

    storage.save()

    return jsonify(amenity_obj.to_dict()), 200
