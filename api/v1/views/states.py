#!/usr/bin/python3
"""
Module for Place objects that handles all default RESTful API actions.
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
    Retrieves a list of all Place objects of a City or creates a Place.
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")
        if 'user_id' not in body:
            abort(400, description="Missing user_id")
        if 'name' not in body:
            abort(400, description="Missing name")

        user = storage.get(User, body['user_id'])
        if not user:
            abort(404)

        place = Place(**body, city_id=city_id)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieves, deletes, or updates a Place object.
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
        body = request.get_json()
        if not body:
            abort(400, description="Not a JSON")

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in body.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    Searches for Place objects based on a JSON payload.
    """
    body = request.get_json()
    if not body:
        abort(400, description="Not a JSON")

    return jsonify([place.to_dict() for place in places])
