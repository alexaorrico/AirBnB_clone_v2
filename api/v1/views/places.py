#!/usr/bin/python3
"""It creates a new view for Place objects"""

from models.place import Place
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """It retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """It retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(places, place_id):
    """It deletes a Place Object"""
    places = storage.get(Place, place_id)
    if not places:
        abort(404)

    storage.delete(places, place_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """It creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, 'Missing user_id')

    data = request.get_json()
    user = storage.get(user, data['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    data["city_id"] = city_id
    new = Place(**data)
    new.save()
    return jsonify(new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """It updates a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    ignore_key = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_key:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
