#!/usr/bin/python3
"""
Defines the places view for the API. This module contains route handlers
for managing Place objects through RESTful API actions.
"""
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_by_city(city_id):
    """
    Handles GET and POST requests for places within a specific city.
    GET: Retrieves a list of all places in the city.
    POST: Creates a new place in the city with the provided JSON request data.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        return jsonify([place.to_dict() for place in city.places])

    if request.method == 'POST':
        request_data = request.get_json(silent=True)
        if request_data is None:
            abort(400, "Not a JSON")
        if 'user_id' not in request_data:
            abort(400, "Missing user_id")
        user = storage.get(User, request_data['user_id'])
        if not user:
            abort(404)
        if 'name' not in request_data:
            abort(400, "Missing name")
        place = Place(**request_data)
        place.city_id = city_id
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places_by_id(place_id):
    """
    Handles GET, DELETE, and PUT requests for a specific place.
    GET: Retrieves a place by its ID.
    DELETE: Deletes a place by its ID.
    PUT: Updates a place by its ID with the provided JSON request data.
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        request_data = request.get_json(silent=True)
        if request_data is None:
            abort(400, "Not a JSON")
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in request_data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
