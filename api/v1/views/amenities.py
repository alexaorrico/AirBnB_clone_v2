#!/usr/bin/python3
"""
returns json response for GET, POST, PUT and DELETE
Methods for Amenities of API
"""
from flask import Flask, jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Get all Amenity objects"""
    amenities = [amenity.to_dict() for amenity
                 in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Get a specific Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    response = request.get_json(silent=True)

    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    """Create a new Amenity object"""
    new_amenity = Amenity(**response)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    response = request.get_json(silent=True)
    if not amenity:
        abort(404)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, value in response.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(amenity.to_dict(), 200)
