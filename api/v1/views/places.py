#!/usr/bin/python3
""" module view for place objects;
handles all default Restful API actions
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from models.place import Place
from . import app_views
import uuid


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_by_city(city_id):
    """gets list of all state objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = city.places
    placess = [place.to_dict() for place in places]
    return jsonify(placess)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id=None):
    """get place by id"""

    # print("Full request: ", request)
    place = storage.get(Place, place_id)
    # print('State id is {}'.format(state_id))
    # print('State id is type {}'.format(type(state_id)))
    # print('State is {}'.format(state))

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place identified by id"""
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create place from http request"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city.id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """updates a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, val)
    place.save()
    return jsonify(place.to_dict()), 200
