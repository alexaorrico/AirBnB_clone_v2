#!/usr/bin/python3
"""objects that handles all default RestFul API actions for Amenities"""

from flask import abort, request, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models import amenity
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False)
def get_amenity():
    """Method for amenity"""
    new_list = []
    for amenity in storage.all(Amenity).values():
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route("/amenities/<string:amenity_id>", strict_slashes=False)
def one_amenity(amenity_id):
    """Method for one amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<string:amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """Method that deletes a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify(({})), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """Method that creates a amenity"""
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if "name" not in data:
        abort(400, description="Missing name")
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/amenities/<string:amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """Method that puts a amenity"""
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()
    if not amenity:
        abort(404)
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
