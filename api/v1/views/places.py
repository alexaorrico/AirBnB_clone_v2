#!/usr/bin/python3
"""
Module for handling RESTful API actions for Place objects.
"""

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """
    Retrieves the list of all Place objects of a City.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description=f"City with ID {city_id} not found")

    places = storage.all(Place).values()
    city_places = [place.to_dict() for place in places
                   if place.city_id == city_id]
    return jsonify(city_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place object.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description=f"City with ID {city_id} not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    if 'name' not in data:
        abort(400, description="Missing name")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404, description=f"User with ID {data['user_id']} not found")

    new_place = Place(city_id=city_id, **data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description=f"Place with ID {place_id} not found")

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200
