#!/usr/bin/python3
"""
Cities CRUD
"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/cities', strict_slashes=False, methods=['GET'])
def all_cities():
    """ Return all cities """
    cities = storage.all("City")
    cities_list = []
    for city in cities.values():
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def city_by_id(city_id):
    """ Return a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ Delete a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', strict_slashes=False, methods=['POST'])
def create_cities(city_id):
    """ Create a city """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    if 'state_id' not in request.json:
        abort(400, 'Missing state_id')
    state = storage.get("State", request.json['state_id'])
    if state is None:
        abort(404)
    city = City(**request.json)
    city.state_id = state.id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_cities(city_id):
    """ Update a city """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
