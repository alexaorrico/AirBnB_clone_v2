#!/usr/bin/python3
"""This module handles all default RESTFul API actions for Amenity objects"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@swag_from('documentation/amenity/all_amenities.yml')
def get_amenities():
    """
    Retrieves the list of all Amenity obj
    """
    amenities = storage.all(Amenity).values()
    list = []
    for amenity in amenities:
        list.append(amenity.to_dict())
    return jsonify(list)


@app_views.route('/amenities/<amenity_id>/', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/amenity/get_amenity.yml', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieves a single amenity obj """
    amenity_d = storage.get(Amenity, amenity_id)
    if not amenity_d:
        abort(404)

    return jsonify(amenity_d.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/amenity/delete_amenity.yml', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes a Amenity obj
    """

    amenity_d = storage.get(Amenity, amenity_id)

    if not amenity_d:
        abort(404)

    storage.delete(amenity_d)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
@swag_from('documentation/amenity/post_amenity.yml', methods=['POST'])
def post_amenity():
    """
    Creates an amenity
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data_amen = request.get_json()
    inst = Amenity(**data_amen)
    inst.save()
    return make_response(jsonify(inst.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/amenity/put_amenity.yml', methods=['PUT'])
def put_amenity(amenity_id):
    """
    Updates amenity obj
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore_key = ['id', 'created_at', 'updated_at']

    amenity_d = storage.get(Amenity, amenity_id)

    if not amenity_d:
        abort(404)

    data_amen = request.get_json()
    for key, value in data_amen.items():
        if key not in ignore_key:
            setattr(amenity_d, key, value)
    storage.save()
    return make_response(jsonify(amenity_d.to_dict()), 200)
