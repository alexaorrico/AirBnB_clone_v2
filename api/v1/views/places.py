#!/usr/bin/python3
"""
    Handles default RestFul API actions for place objects
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User


@app_views.route(
    '/cities/<city_id>/places',
    methods=['GET', 'POST'],
    strict_slashes=False
)
def places_all(city_id):
    """
        Handle all objects
    """
    list_of_places = []
    objects = storage.all(Place).values()
    for obj in objects:
        list_of_places.append(obj.to_dict())

    if request.method == 'GET':
        return jsonify(list_of_places)

    if request.method == 'POST':

        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        if 'name' not in request_dict.keys():
            abort(400, 'Missing name')

        if 'user_id' not in request_dict.keys():
            abort(400, 'Missing user_id')

        new_place = Place(**request_dict)
        new_place.save()

        return jsonify(new_place.to_dict()), 201


@app_views.route(
    '/places/<place_id>',
    methods=['GET', 'PUT', 'DELETE'],
    strict_slashes=False
)
def places_by_id(place_id):
    """
        Handle objects by ID
    """

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        place_obj.delete()
        storage.save()
        return {}, 200

    if request.method == 'PUT':
        try:
            request_dict = request.get_json()
        except:
            abort(400, 'Not a JSON')

        user_obj = storage.get(User, place_obj.user_id)
        if user_obj is None:
            abort(404)

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in request_dict.items():
            if key in ignore_keys:
                continue
            setattr(place_obj, key, value)
        place_obj.save()

        return jsonify(place_obj.to_dict()), 200
