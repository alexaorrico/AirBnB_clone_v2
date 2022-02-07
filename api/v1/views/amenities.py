#!/usr/bin/python3
"""view for Amenitites objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities/', strict_slashes=False)
def all_amenities():
    """Retrieves all amenitoes"""
    amenities = storage.all('Amenity')
    new_list = []
    for amenity in amenities.values():
        new_list.append(amenity.to_dict())
    return jsonify(new_list)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieves a amenity by a given ID"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False
    )
def create_amenity():
    """Creates a Amenity object"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request_data:
        return jsonify({"error": "Missing name"}), 400
    obj = Amenity(**request_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def update_amenity(amenity_id):
    """Update a Amenity object"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
