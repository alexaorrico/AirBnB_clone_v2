#!/usr/bin/python3
"""
    Handles API requests for Amenity
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities():
    """
        Retrieves Amenities
    """
    if request.method == 'GET':
        amenity_list = []
        for amenity in storage.all(Amenity).values():
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)
    if request.method == 'POST':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        if 'name' not in info:
            abort(400, 'Missing name')
        new_amenity = Amenity(**info)
        new_amenity.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def spec_amenity(amenity_id):
    """
        Works with an amenity with a specified id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        info = request.get_json(silent=True)
        if not info:
            abort(400, 'Not a JSON')
        for key, value in info.items():
            if key in ['id', 'created_at', 'updated_at']:
                pass
            else:
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 200
