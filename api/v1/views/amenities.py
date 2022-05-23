#!/usr/bin/python3
""" view for Amenity objects that handles all default RESTFul API actions """

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def Amenitys():
    """ Retrieves the list of all Amenity objects and create a new Amenity"""

    # retrieves Amenity object
    if request.method == 'GET':
        Amenitys = storage.all(Amenity)
        Amenitys_list = []
        for key, value in Amenitys.items():
            Amenitys_list.append(value.to_dict())
        return jsonify(Amenitys_list)

    # create a Amenity
    elif request.method == 'POST':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # If the dictionary doesn’t contain the key name
        if 'name' not in body_request_dict:
            abort(400, 'Missing name')

        # create new object Amenity with body_request_dict
        new_Amenity = Amenity(**body_request_dict)

        storage.new(new_Amenity)
        storage.save()
        return new_Amenity.to_dict(), 201


@app_views.route('/Amenitys/<Amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def Amenity_id(Amenity_id):
    """
        Retrieves a Amenity object
    """
    Amenity_catch = storage.get(Amenity, Amenity_id)

    # If the Amenity_id is not linked to any Amenity object, raise a 404 error
    if Amenity_catch is None:
        abort(404)

    # Retrieves a Amenity object
    if request.method == 'GET':
        return Amenity_catch.to_dict()

    # Deletes a Amenity object
    if request.method == 'DELETE':
        empty_dict = {}
        storage.delete(Amenity_catch)
        storage.save()
        return empty_dict, 200

    # update a Amenity object
    if request.method == 'PUT':
        # transform the HTTP body request to a dictionary
        body_request_dict = request.get_json()

        # If the HTTP body request is not valid JSON
        if not body_request_dict:
            abort(400, 'Not a JSON')

        # Update the Amenity object with all key-value pairs of the dictionary
        # Ignore keys: id, created_at and updated_at

        for key, value in body_request_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(Amenity_catch, key, value)

        Amenity_catch.save()
        return Amenity_catch.to_dict(), 200
