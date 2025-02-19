#!/usr/bin/python3
"""Modle handles all default RESTful API actions for Amenity objects"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False, endpoint='all_amenities')
def all_amenities():
    """Retrieves the lisf of all Amenity objects"""
    amenities = storage.all(Amenity)
    list_of_amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(list_of_amenities), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False, endpoint='get_amenity')
def get_amenity(amenity_id):
    """Retrieves an Amenity object using the id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='delete_amenity')
def delete_amenity(amenity_id):
    """Deletes an Amenity object from storage"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False,
                 endpoint='create_amenity')
def create_amenity():
    """Creates an Amenity object"""
    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    if not json_data.get('name'):
        abort(400, description='Missing name')

    amenity = Amenity(**json_data)

    storage.new(amenity)
    storage.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False, endpoint='update_amenity')
def update_amenity(amenity_id):
    """Update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
