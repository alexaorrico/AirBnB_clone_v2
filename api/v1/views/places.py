#!/usr/bin/python3
"""Handles RESTful API actions for Place objects."""
from flask import abort, jsonify, request
from api.v1.views import app_views
from models import storage, City, Place, User


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """function retrieves all the places belonging to a
    city and returns them as a JSON response."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """function retrieves a place by its ID
    and returns it as a JSON response."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """function deletes a place by its ID and returns an
    empty JSON response with a status code of 200."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """function creates a new place in a city specified
    by its ID. It checks that the request body is valid
    JSON, contains a valid user ID, and a name for the
    place. It returns the newly created place as a JSON
    response with a status code of 201."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    user_id = data.get('user_id')
    if user_id is None:
        abort(400, 'Missing user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    name = data.get('name')
    if name is None:
        abort(400, 'Missing name')
    place = Place(name=name, user_id=user_id, city_id=city_id)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """function updates a place specified by
    its ID with the values specified in the
    request body. It ignores the ID, user ID,
    city ID, created_at, and updated_at fields.
    It returns the updated place as a JSON response
    with a status code of 200."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
