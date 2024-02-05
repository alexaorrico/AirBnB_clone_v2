#!/usr/bin/python3
"""
Contains the amenities view for the AirBnB clone v3 API.
Handles all default RESTful API actions for Amenity objects.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects.
    """
    all_amenities = storage.all(Amenity).values()
    amenities_list = [amenity.to_dict() for amenity in all_amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates an Amenity.
    """
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    if 'name' not in request_data:
        abort(400, description='Missing name')
    new_amenity = Amenity(**request_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, description='Not a JSON')
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
