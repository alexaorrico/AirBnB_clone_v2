#!/usr/bin/python3
"""
handles all default RESTful API actions
"""

from models.amenity import Amenity
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_all_amenities():
    """
    gets the list of all Amenity obj
    """
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenity_list)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity obj

    Args:
        amenity_id(int): id for amenity.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity obj

    Args:
        amenity_id(int): id for amenity.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates an Amenity obj
    """
    if not request.json:
        abort(400, 'Not a JSON')

    data = request.json
    if 'name' not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an Amenity obj

    Args:
        amenity_id(int): id for amenity.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if not request.json:
        abort(400, 'Not a JSON')

    data = request.json
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_dict()), 200


@app_views.errorhandler(404)
def not_found(error):
    """
    Returns 404: Not Found

    Args:
        error: error
    """
    return jsonify({'error': 'Not found'}), 404


@app_views.errorhandler(400)
def bad_request(error):
    """
    Return Bad Request message

    Args:
        error: error
    """
    return jsonify({'error': 'Bad Request'}), 400
