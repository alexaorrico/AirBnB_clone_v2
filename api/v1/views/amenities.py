#!/usr/bin/python3
"""Flask Api Amenity module"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def amenities():
    """Retrieve all amenities"""
    amenities = [amenity.to_dict() for amenity in storage.all(
                 Amenity).values()]
    return jsonify(amenities), 200


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve an amenity based on its amenity_id, return 404 if not found"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an amenity based on its amenity_id or return 404 if not found"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """Creates a new amenity or return 404 if not found"""
    if not request.is_json:
        abort(400, "Not a JSON")
    obj = request.get_json()
    if 'name' not in obj:
        abort(400, "Missing name")
    amenity = Amenity(**obj)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id: str = None):
    """Update an amenity given its id or return 404 if not found"""
    if not request.is_json:
        abort(400, "Not a JSON")
    obj = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for key, value in obj.items():
        if key not in ('id', 'updated_at', 'created_at'):
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
