#!/usr/bin/python3
"""handles all defaults RESTful API actions for states"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """retrieve all amenities"""
    amenities = storage.all(Amenity)
    amenities_list = []

    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """retrieves a amenity based on its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    return abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes a amenity based on its id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creates a new amenity"""
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    if "name" not in data:
        return abort(400, "Missing name")
    amenity = Amenity()
    amenity.name = data["name"]
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates a given amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return abort(404)
    data = request.get_json()
    if data is None:
        return abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
