#!/usr/bin/python3
"""
Module for handling RESTful API actions for Amenity objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description=f"Amenity with ID {amenity_id} not found")
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description=f"Amenity with ID {amenity_id} not found")
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates a Amenity.
    """
    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if not data:
        abort(400, description="Not a JSON")

    if "name" not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, description=f"Amenity with ID {amenity_id} not found")

    try:
        data = request.get_json()
    except Exception as e:
        abort(400, description="Not a JSON")

    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
