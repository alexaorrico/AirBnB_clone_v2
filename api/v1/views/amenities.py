#!/usr/bin/python3
""" New view for amenities object that handles all
default RESTFul API actions. """
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_amenities():
    """ Retrieves the list of all Amenity objects
    or creates a new one.
    """
    if request.method == 'GET':
        all_amenities = storage.all(Amenity).values()
        list_amenities = [amenity.to_dict() for amenity in all_amenities]
        return jsonify(list_amenities)

    if request.method == 'POST':
        req_data = request.get_json()
        if not req_data:
            abort(400, description="Not a JSON")

        if 'name' not in req_data:
            abort(400, description="Missing name")

        amenity = Amenity(**req_data)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_amenity_id(amenity_id):
    """ Retrieves, deletes or updates an Amenity object given its id.
    Returns 404 error if id is not found.
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == 'PUT':
        req_data = request.get_json()
        if not req_data:
            abort(400, description='Not a JSON')

        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in req_data.items():
            if key not in ignore_keys:
                setattr(amenity, key, value)

        storage.save()
        return make_response(jsonify(amenity.to_dict()), 200)
