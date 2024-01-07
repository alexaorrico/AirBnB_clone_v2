#!/usr/bin/python3
"""
a new view for Amenity objects that handles all default RESTFul API actions.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'])
def amenity_by_id(amenity_id):
    """
    Retrieves, updates, or deletes a Amenity object by ID.

    GET /api/v1/amenities/<amenity_id> - Retrieves a Amenity object.
    PUT /api/v1/amenities/<amenity_id> - Updates a Amenity object.
    DELETE /api/v1/amenities/<amenity_id> - Deletes a Amenity object.

    Args:
    amenity_id (str): ID of the Amenity.

    Returns:
    JSON: Amenity obj or success message.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.metod == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200
