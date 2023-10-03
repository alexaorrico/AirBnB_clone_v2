#!/usr/bin/python3
"""Amenities view"""

from flask import Flask, jsonify, request, abort
from models import storage, Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve the list of all Amenity objects."""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new Amenity."""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object by ID."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    data.pop("id", None)
    data.pop("created_at", None)
    data.pop("updated_at", None)
    for key, value in data.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
