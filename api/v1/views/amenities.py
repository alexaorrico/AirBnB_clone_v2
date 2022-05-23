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
        amenities = storage.all('Amenity')

        for amenity in amenities.values():
            amenitiesList.append(amenity.to_dict())

        return jsonify(amenitiesList)

    elif request.method == 'POST':
        requestDict = request.get_json()

        if not requestDict:
            abort(400, 'Not a JSON')

        if "name" not in requestDict:
            abort(400, 'Missing name')

        newAmenity = Amenity(**requestDict)
        storage.new(newAmenity)
        storage.save()

        return newAmenity.to_dict(), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
def amenities_amenity_id(amenity_id):
    """
        Retrieves a amenities object
    """
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    if request.method == 'GET':
        return amenity.to_dict()

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        requestDict = request.get_json()

        if not requestDict:
            return 'Not a JSON', 400

        ignoredList = ["id", "created_at", "updated_at"]
        for key, value in requestDict.items():
            if key not in ignoredList:
                setattr(amenity, key, value)

        amenity.save()
        return amenity.to_dict(), 200
