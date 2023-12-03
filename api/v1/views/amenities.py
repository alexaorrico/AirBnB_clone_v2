#!/usr/bin/python3

"""
Module for handling HTTP requests related to Amenity objects
"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, make_response, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    Retrieve all amenities
    """
    all_amenities = storage.all(Amenity)
    res = []
    for amenity in all_amenities.values():
        res.append(amenity.to_dict())
    return jsonify(res)


@app_views.route("/amenities/<string:amenity_id>", methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieve an amenity with the given id
    """
    instance = storage.get(Amenity, amenity_id)
    if instance is None:
        abort(404)
    return jsonify(instance.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """
    Delete an amenity with the given id
    """
    instance = storage.get(Amenity, amenity_id)
    if instance is None:
        abort(404)
    storage.delete(instance)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """
    Create a new amenity
    """
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    if 'name' not in res:
        abort(400, 'Missing name')
    instance = Amenity(**res)
    instance.save()
    return jsonify(instance.to_dict()), 201


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """
    Update an amenity with the given id
    """
    instance = storage.get(Amenity, amenity_id)
    if instance is None:
        abort(404)
    res = request.get_json()
    if res is None:
        abort(400, 'Not a JSON')
    for idx, idy in res.items():
        setattr(instance, idx, idy)
    instance.save()
    return jsonify(instance.to_dict())
