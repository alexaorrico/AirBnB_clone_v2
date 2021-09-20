#!/usr/bin/python3
"""handles all default RESTFul API actions"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id=None):
    """liste all cities of a state"""
    list_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        list_cities.append(city.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id=None):
    """get one city"""
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id=None):
    """ Delete a city"""
    if city_id is None:
        abort(404)
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def add_city(state_id=None):
    """add a city to a state"""
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    if 'name' not in requeste.keys():
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    requeste['state_id'] = state_id
    new_city = City(**requeste)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id=None):
    """update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    requeste = request.get_json()
    if requeste is None:
        abort(400, "Not a JSON")
    for key, value in requeste.items():
        setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
