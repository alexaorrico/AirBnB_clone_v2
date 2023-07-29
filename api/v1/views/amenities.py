#!/usr/bin/python3
"""amenity obj API"""
from flask import Flask, jsonify, abort, make_response, request
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id=None):
    """Get all amenities or a amenities whose id is specified"""
    if amenity_id is None:
        amenities = storage.all(Amenity).values()
        amenities_list = [amenity.to_dict() for amenity in amenities]
        return jsonify(amenities_list)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new amenity"""
    amenity = request.get_json()
    if not amenity:
        abort(400, description="Not a JSON")
    if 'name' not in amenity:
        abort(400, description="Missing name")
    obj = Amenity(**amenity)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    fixed_data = ['id', 'created_at', 'updated_at']
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    for key, value in data.items():
        if key not in fixed_data:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
