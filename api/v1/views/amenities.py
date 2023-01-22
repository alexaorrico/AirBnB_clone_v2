#!/usr/bin/python3
"""ALX SE Flask Api Amenity Module."""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def get_amenitys():
    """Return list of all amenitys."""
    amenitys = [state.to_dict() for state in storage.all(Amenity).values()]
    return jsonify(amenitys)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False)
def get_amenity(amenity_id: str):
    """Return a amenity given its id or 404 when not found."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        '/amenities/<string:amenity_id>',
        methods=['DELETE'],
        strict_slashes=False)
def delete_amenity(amenity_id: str):
    """Delete a amenity given its id or 404 when not found."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new amenity."""
    try:
        amenity_attrs = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in amenity_attrs:
        abort(400, "Missing name")
    amenity = Amenity(**amenity_attrs)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
        '/amenities/<string:amenity_id>',
        methods=['PUT'],
        strict_slashes=False)
def update_amenity(amenity_id: str):
    """Update a amenity given its id."""
    try:
        amenity_attrs = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for key, value in amenity_attrs.items():
        if key not in ('id', 'updated_at', 'created_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
