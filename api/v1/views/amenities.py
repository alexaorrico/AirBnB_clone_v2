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
def amenities_show(amenity_id) -> json:
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
