#!/usr/bin/python3
"""
    view for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def amenities():
    """
        Retrieves the list of all amenities objects and create a new amenities"
    """

    if request.method == 'GET':
        amenitiesList = []
        amenities = storage.all(Amenity)

        for amenity in amenities.values():
            amenitiesList.append(amenity.to_dict())

        return jsonify(amenitiesList)

    elif request.method == 'POST':
        body_request_dict = request.get_json()

        if not body_request_dict:
            abort(400, 'Not a JSON')

        if "name" not in body_request_dict:
            abort(400, 'Missing name')

        newAmenity = Amenity(**body_request_dict)
        storage.new(newAmenity)
        storage.save()

        return newAmenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_amenity_id(amenity_id):
    """
        Retrieves a amenities object
    """
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return amenity.to_dict()

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        body_request_dict = request.get_json()

        if not body_request_dict:
            return 'Not a JSON', 400

        for key, value in body_request_dict.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(amenity, key, value)

        amenity.save()
        return amenity.to_dict(), 200
