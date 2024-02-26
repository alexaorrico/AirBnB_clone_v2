#!/usr/bin/python3

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage, Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrieves the list of all Amenity objects."""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """Retrieves an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an Amenity."""
    if not request.get_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    data = request.get_json
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Updates an Amenity object."""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    data = request.get_json
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
