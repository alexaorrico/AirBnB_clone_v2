#!/usr/bin/python3
"""
Module for view for Place objects
It handles all default RESTful API actions
"""

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_list(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        abort(400, 'Missing name')

    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignored_keys:
            setattr(place, key, value)

    storage.save()

    return jsonify(place.to_dict())
