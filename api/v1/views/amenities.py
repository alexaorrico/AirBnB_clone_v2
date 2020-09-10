#!/usr/bin/python3
"""
    Handles default RestFul API actions for Amenity objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def amenities_all():
    """
        Handle all objects
    """
    list_of_amenities = []
    objects = storage.all(Amenity).values()
    for obj in objects:
        list_of_amenities.append(obj.to_dict())

    if request.method == 'GET':
        return jsonify(list_of_amenities)

    if request.method == 'POST':

        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        if 'name' not in request_dict.keys():
            abort(400, 'Missing name')

        new_amenity = Amenity(**request_dict)
        new_amenity.save()

        return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False
)
def amenities_by_id(amenity_id):
    """
        Handle objects by ID
    """

    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(amenity_obj.to_dict())

    if request.method == 'DELETE':
        amenity_obj.delete()
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in request_dict.items():
            if key in ignore_keys:
                continue
            setattr(amenitry_obj, key, value)
        amenity_obj.save()

        return jsonify(amenity_obj.to_dict()), 200
