#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.vi.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retreive the list of all amenities objects"""
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slasheds=False)
def get_amenity(amenity_id):
    """Retrieve the specific amenity object by Id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slasheds=False)
def delete_amenity(amenity_id):
    """Delete a Amenity object by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slasheds=False)
def create_amenity():
    """Create a new amenity object"""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slasheds=False)
def update_amenity(amenity_id):
    """Update a Amenity Object by ID"""
    if amenity:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Not a Json"}), 400
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)


        amenity.save()
        return jsonify(amenity.to_dict()), 200
    else:
        abort(404)
