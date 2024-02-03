#!/usr/bin/python3
'''routes for City objects'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    '''Retrieve all City objects of a State'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''Retrieve a City object'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    '''Delete a City object'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return {}, 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    '''Create a City object'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    city = City(state_id=state_id, **data)
    storage.new(city)
    storage.save()

    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''Update a City object'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    try:
        data = request.get_json()
    except json.JSONDecodeError:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
