#!/usr/bin/python3
"""
Amenity view objects that handle RESTFul API
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
import models
from models import storage
from models.place import Place
from models.user import User
from models.city import City


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get(city_id):
    """Get list of place obj of a city"""
    city = storage.all(City)
    id = f"City.{city_id}"
    if id not in city:
        abort(404)

    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            places_list = place.to_dict()
    return jsonify(places_list)


@app_views.route('/places/<place_id>/places', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get list of place obj"""
    place = storage.all(Place)
    id = f"Place.{place_id}"
    if id not in place:
        abort(404)

    p = place[id]
    return jsonify(p.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete(place_id):
    """Deletes place obj"""

    places = storage.all(Place)
    id = f'Place.{place_id}'
    if id not in places:
        abort(404)

    place = places[id]
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post(city_id):
    """Creates a place obj"""

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    city = storage.all(City)
    id = f"City.{city_id}"
    if id not in city:
        abort(400)

    user = storage.all(User)
    id = f"User.{data['user_id']}"
    if id not in user:
        abort (404)
    if 'name' not in data:
        abort(400, 'Missing name')

    place = Place(name=data['name'], user_id=data['user_id'], city_id=city_id)
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put(place_id):
    """Upgrades an place obj"""

    place = storage.all(Place)
    id = f"Place.{place_id}"
    if id not in place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200