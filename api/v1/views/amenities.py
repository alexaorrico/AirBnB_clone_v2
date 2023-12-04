#!/usr/bin/python3

"""
Module for handling HTTP requests for Amenity objs
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, make_response, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Amenities retrieved
    """
    all_amenities = storage.all(Amenity)
    result = []
    for amenity in all_amenities.values():
        result.append(amenity.to_dict())
    return jsonify(result)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """
    Retrieve an amenity using specified id
    """
    instance = storage.get(Amenity, amenity_id)
    if instance is None:
        abort(404)
    return jsonify(instance.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """
    Delete an amenity of a given id
    """
    instance = storage.get(Amenity, amenity_id)
    if instance is None:
        abort(404)
    storage.delete(instance)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates new amenity
    """
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    if 'name' not in result:
        abort(400, 'Missing name')
    instance = Amenity(**result)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity_id(amenity_id):
    """
    Update an amenity of a specified id
    """
    instance = storage.get(Amenity, amenity_id)
    if instance is None:
        abort(404)
    result = request.get_json()
    if result is None:
        abort(400, 'Not a JSON')
    for idx, idy in result.items():
        setattr(instance, idx, idy)
    instance.save()
    return jsonify(instance.to_dict())
