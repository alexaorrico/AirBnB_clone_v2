#!/usr/bin/python3
"""
a new view for Place objects that handles all default RESTFul API actions.
"""

from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def get_place_or_update_place(place_id):
    """
    Retrieves, updates, or deletes a Place object by ID.

    GET /api/v1/places/<place_id> - Retrieves a Place object.
    PUT /api/v1/places/<place_id> - Updates a Place object.
    DELETE /api/v1/places/<place_id> - Deletes a Place object.

    Args:
    place_id (str): ID of the Place.

    Returns:
    JSON: Place obj or success message.
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'PUT':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_places_or_create_place(city_id):
    """
    Retrieves the list of all Place objects of a City or creates a new Place.

    GET /api/v1/cities/<city_id>/places - Retrieves places of a city.
    POST /api/v1/cities/<city_id>/places - Creates a new Place.

    Args:
    city_id (str): ID of the City.

    Returns:
    JSON: List of Place objects or newly created Place.
    """
    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    if request.method == 'GET':
        places = [place.to_dict() for place in city.places]
        return jsonify(places)

    if request.method == 'POST':
        try:
            data = request.get_json()
        except Exception:
            abort(400, 'Not a JSON')

        if data is None:
            abort(400, 'Not a JSON')

        if 'user_id' not in data:
            abort(400, 'Missing user_id')

        user = storage.get(User, data['user_id'])
        if 'name' not in data:
            abort(400, 'Missing name')

        new_place = Place(**data)
        new_place.city_id = city_id
        new_place.save()
        return jsonify(new_place.to_dict()), 201
