#!/usr/bin/python3
"""this is for amenities amenities.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieve information for all unique amenities"""
    unique_amenities_list = []
    for unique_amenity_instance in storage.all("Amenity").values():
        unique_amenities_list.append(unique_amenity_instance.to_dict())
    return jsonify(unique_amenities_list)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve information for specified amenity"""
    unique_amenity_instance = storage.get("Amenity", amenity_id)
    if unique_amenity_instance is None:
        abort(404)
    return jsonify(unique_amenity_instance.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity based on its unique_amenity_id"""
    unique_amenity_instance = storage.get("Amenity", amenity_id)
    if unique_amenity_instance is None:
        abort(404)
    unique_amenity_instance.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Create a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Update an amenity"""
    unique_amenity_instance = storage.get("Amenity", amenity_id)
    if unique_amenity_instance is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(unique_amenity_instance, attr, val)
    unique_amenity_instance.save()
    return jsonify(unique_amenity_instance.to_dict())
