#!/usr/bin/python3
""" Handles all default RESTful API action
"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
def get_amenities():
    """
    Get all amenities from the storage and return them as a JSON response.

    Returns:
            - A JSON response containing a list of all amenities.
            - A status code of 200 if the request was successful.
    """
    amenities = storage.all("Amenity")
    amenities_list = []
    for amenity in amenities.values():
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['GET'])
def get_amenity(amenity_id):
    """
    Get a amenity by its ID.

    :param amenity_id: The ID of the amenity to retrieve.
    :return: A JSON response containing the amenity information.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity.to_dict()), 200


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes a amenity from the database.

    :param amenity_id: The ID of the amenity to be deleted.
    :type amenity_id: int
    :return: A JSON response indicating the success of the deletion.
    :rtype: dict
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def post_amenity():
    """
    Creates a new amenity.

    :return: A JSON response indicating the success of the creation.
    :rtype: dict
    """
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, description="Not a JSON")
    if 'name' not in amenity_data:
        abort(400, description="Missing name")
    amenity = Amenity(**amenity_data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>', strict_slashes=False, methods=['PUT'])
def put_amenity(amenity_id):
    """
    Updates a amenity in the database.

    :param amenity_id: The ID of the amenity to be updated.
    :type amenity_id: int
    :return: A JSON response indicating the success of the update.
    :rtype: dict
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_data = request.get_json()
    if not amenity_data:
        abort(400, description="Not a JSON")
    for key, value in amenity_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
