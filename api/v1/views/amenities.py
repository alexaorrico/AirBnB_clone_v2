#!/usr/bin/python3
"""
Handles RESTFul API actions for amenities
"""

from flask import abort
from api.v1.views import app_views
from flask import jsonify
from flask import request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """
    Returns list of all amenities
    """
    amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route("/amenities/<amenity_id>", methods=['GET'],
                 strict_slashes=False)
def one_amenity(amenity_id):
    """
    Returns an amenity object based on id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an amenity object based on id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def add_amenity():
    """
    Adds an amenity object based on data provided
    """
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an amenity object based on data provided
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
        keys_to_ignore = ["created_at", "id", "updated_at"]
        for k, v in data.items():
            if k not in keys_to_ignore:
                amenity.__dict__.update({k: v})
        storage.save()
        return jsonify(amenity.to_dict()), 200
    abort(404)
