#!/usr/bin/python3
"""
Module that houses the view for Amenity objects
It handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenity_list():
    """Retrieves the list of all Amenity objects"""
    amenities_list = []
    amenities = storage.all(Amenity).values()
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_obj(amenity_id):
    """
    Retrieves an Amenity object

    Args:
        amenity_id: The id of the amenity object
    Raises:
        404: if amenity_id supplied is not linked to any amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict()), 200
    else:
        return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenities_obj(amenity_id):
    """
    Deletes an Amenity object

    Args:
        amenity_id: The id of the amenity object
    Raises:
        404: if amenity_id supplied is not linked to any amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({"error": "Not found"}), 404
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'], strict_slashes=False)
def post_amenity():
    """
    Creates an Amenity object

    Returns:
        The new State with the status code 201
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates an Amenity object

    Args:
        amenity_id: The id of the amenity object
    Raises:
        404:
            If amenity_id supplied is not linked to any amenity o    bject
            400: If the HTTP body request is not valid JSON
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        return jsonify({'error': 'Not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400
    data.pop('id', None)
    data.pop('created_at', None)
    data.pop('updated_at', None)
    for key, value in data.items():
        setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
