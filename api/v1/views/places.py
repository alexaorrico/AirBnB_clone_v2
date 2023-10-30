#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
        )
def list_places_of_city(city_id):
    '''Retrieves a list of all Place objects in city'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    res = jsonify(places)
    return res


@app_views.route(
        '/places/<place_id>', methods=['GET'], strict_slashes=False
        )
def get_place(place_id):
    '''Retrieves a Place object'''
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_dict())


@app_views.route(
        '/places/<place_id>', methods=['DELETE'], strict_slashes=False
        )
def delete_place(place_id):
    '''Deletes a Place object'''
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    storage.save()
    res = jsonify({})
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False
        )
def create_place(city_id):
    '''Creates a Place'''
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    user = storage.get("User", str(data["user_id"]))
    if user is None:
        abort(404)

    data["city_id"] = str(city_id)
    new_place = Place(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
        '/places/<place_id>', methods=['PUT'], strict_slashes=False
        )
def updates_place(place_id):
    '''Updates a Place object'''

    place_obj = storage.get("Place", place_id)

    if place_obj is None:
        abort(404)

    data = request.get_json(silent=True)

    if data is None:
        abort(400, 'Not a JSON')

    for k, v in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, k, v)

    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
