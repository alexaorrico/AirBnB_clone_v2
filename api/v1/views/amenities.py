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
    Retrieves the list of all State objects.

    Returns:
        json: List of State objects with status code 200.
    """
    amenities = storage.all(Amenity)
    list = []
    for key, amenity in amenities.items():
        list.append(amenity.to_dict())
    return make_response(jsonify(list), 200)
