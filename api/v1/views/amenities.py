#!/usr/bin/python3
"""
Route for handling Amenity objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage, Amenity

@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """Retrieves all Amenity objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def amenity_get_by_id(amenity_id):
    """Retrieves a specific Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """Deletes a specific Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """Creates a new Amenity"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def amenity_update(amenity_id):
    """Updates a specific Amenity object by ID"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
