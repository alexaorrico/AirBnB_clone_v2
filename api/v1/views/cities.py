#!/bin/bash/python3
"""
"""
from models.state import State
from models.city import City
from models import storage
from flask import abort
from flask import jsonify
from flask import request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """Gets all cities"""
    all_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = storage.all("City").values()
    for city in cities:
        all_cities.append(city.to_dict())
    return jsonify(all_cities)


@app_views.route('cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city(city_id):
    """Retrieves a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return ({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def make_city(state_id):
    """Makes a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city_name = request.get_json()
    if city_name is None:
        abort(400, 'not a JSON')
    if 'name' not in city_name:
        abort(400, 'Missing Name')
    city = City(**city_name)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city_name = request.get_json()
    if not request.get_json():
        abort(400, 'not a JSON')
    for key, value in city_name.items():
        if key in ['id', 'state_id', 'created_at', 'updated_at']:
            pass
        else:
            setattr(city, key, value)
    storage.save()
    all_cities = city.to_dict()
    return jsonify(all_cities), 200
