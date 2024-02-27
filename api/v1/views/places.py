#!/usr/bin/python3
"""Place View"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, Place, City, User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    user = storage.get(User, request.json['user_id'])
    if not user:
        abort(404)
    place = Place(**request.json)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    ignored_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in request.json.items():
        if key not in ignored_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict())
