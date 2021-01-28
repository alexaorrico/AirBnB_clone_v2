#!/usr/bin/python3
"""Places objects that handles all default RestFul API actions
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_of_city(city_id):
    """Retrieve a list of places objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places_in_city = [places.to_dict() for places in city.places]
    return jsonify(places_in_city)


@app_views.route('places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a specific place object """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Create a Place object"""
    if request.get_json() is None:
        return "Not a JSON", 400
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if 'user_id' not in request.get_json():
        return "Missing user_id", 400
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        return "Missing name", 400

    place = Place(**request.get_json())
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def Update_place(place_id):
    """Update a place store in the storage"""
    if request.get_json() is None:
        return "Not a JSON", 400
    place = storage.get(Place, place_id)
    if place:
        ignore_keys = ['id', 'user_id', 'city_id' 'created_at', 'updated_at']
        for key, value in request.get_json().items():
            if key not in ignore_keys:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)
