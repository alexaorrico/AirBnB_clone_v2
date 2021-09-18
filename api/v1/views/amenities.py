#!/usr/bin/python3
"""
    API view related to Amenity objects that handles all the default
    actions.
"""
import requests
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json
from werkzeug.exceptions import BadRequest, NotFound
from flask import Flask, request, jsonify, make_response, abort


def __is_valid_json(data):
    """
    Checks if the given data is a valid json.

    Args:
        data : Data to check

    Returns:
        True: If data is a valid json.
        False: If data is not a valid json.
    """
    try:
        json.loads(data)

        return True
    except Exception:
        return False


@app_views.route('/amenities', methods=['GET'])
def amenities_list() -> json:
    """
    Retrieves the list of all Amenity objects.

    Returns:
        json: List of Amenity objects with status code 200.
    """
    amenities = storage.all(Amenity)
    list = []
    for key, amenity in amenities.items():
        list.append(amenity.to_dict())
    return make_response(jsonify(list), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_show(amenity_id) -> json:
    """
    Retrieves a specified Amenity object.

    Args:
        amenity_id : ID of the wanted Amenity object.

    Raises:
        NotFound: Raises a 404 error if amenity_id
        is not linked to any Amenity object.

    Returns:
        json: Wanted Amenity object with status code 200.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        raise NotFound

    return make_response(jsonify(amenity.to_dict()), 200)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id) -> json:
    """
    Deletes a specified Amenity object.

    Args:
        amenity_id : ID of the wanted Amenity object.

    Raises:
        NotFound: Raises a 404 error if amenity_id
        is not linked to any Amenity object.

    Returns:
        json: Empty dictionary with the status code 200.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        raise NotFound

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities/', methods=['POST'])
def amenity_create() -> json:
    """
    Creates a new Amenity object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new Amenity with the status code 201.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)

    if 'name' not in data.keys():
        return make_response('Missing name', 400)

    amenity = Amenity(data)
    for key, value in data.items():
        amenity.__setattr__(key, value)
    storage.new(amenity)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_update(amenity_id) -> json:
    """
    Update a specified Amenity object.

    Args:
        amenity_id : Id of the wanted Amenity object.

    Returns:
        json: The updated Amenity object with the status code 200.
    """
    data = request.get_data()

    if not __is_valid_json(data):
        return make_response('Not a JSON', 400)

    data = json.loads(data)
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        raise NotFound

    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            amenity.__setattr__(key, value)

    storage.new(amenity)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
