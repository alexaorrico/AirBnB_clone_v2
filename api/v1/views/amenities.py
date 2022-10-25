#!/usr/bin/python3
"""
a new view for Amenity objects that handles
all default RESTFul API actions
"""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify, request
from models import storage
from models.amenity import Amenity
from werkzeug.exceptions import BadRequest, NotFound


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_amenities():
    """
    Retrieves the list of all Amenity objects

    Returns:
        json: Wanted Amenity object with status code 200.
    """
    amenities = storage.all(Amenity)
    amenities_list = []

    for amenity in amenities.items():
        amenities_list.append(amenity.to__dict())
    return make_response(jsonify(amenities_list), 200)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False
)
def single_amenity(amenity_id):
    """
    Retrieves a specified Amenity object.

    Args:
        amenity_id : ID of the specified Amenity object.

    Raises:
        NotFound: Raises a 404 error if amenity_id
        is not linked to any Amenity object.

    Returns:
        json: Wanted Amenity object with status code 200.
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        raise NotFound

    return make_response(jsonify(amenity.to__dict()), 200)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_amenity(amenity_id):
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


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """
    Creates a new Amenity object.

    Error cases:
        BadRequest: If the given data is not a
        valid json or if the key 'name' is not
        present sends status code 400.

    Returns:
        json: The new Amenity with the status code 201.
    """
    amenity = Amenity(**request.get_json())

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if 'name' not in request.get_json.keys():
        return make_response('Missing name', 404)

    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_amenity(amenity_id):
    """
    Update a specified Amenity object.

    Args:
        amenity_id : Id of the wanted Amenity object.

    Returns:
        json: The updated Amenity object with the status code 200.
    """
    amenity = storage.get(Amenity, amenity_id)

    if not request.get_json:
        return make_response('Not a JSON', 400)

    if amenity is None:
        raise NotFound

    for key, amen in request.get_json().items():
        if key not in ('id', 'created_at', 'updated_at'):
            amenity.__setattr__(key, amen)

    amenity.save()

    return make_response(jsonify(amenity.to__dict()), 200)
