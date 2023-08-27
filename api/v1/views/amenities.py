#!/usr/bin/python3
"""Amenities View"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity)
    amenities_list = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                strict_slashes=False)
def create_amenity():
    """Creates a Amenity"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
