#!/usr/bin/python3
'''
Handles all default RESTFul API actions for city objects
'''

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    '''handles GET for all cities objects of a state'''

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    cities_list = [city.to_dict() for city in state_obj.cities]
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    '''handles GET for a city object'''

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    city_dict = city_obj.to_dict()
    return jsonify(city_dict)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    '''deletes a city object'''

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'], strict_slashes=False)
def create_city(state_id):
    '''creates a city object'''

    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    elif 'name' not in json_data.keys():
        return jsonify({"error": "Missing name"}), 400

    new_obj = City()
    new_obj.state_id = state_id
    for attr, val in json_data.items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(new_obj, attr, val)
    new_obj.save()

    return jsonify(new_obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    '''updates a city object'''

    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    json_data = request.get_json()
    if json_data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for attr, val in json_data.items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_obj, attr, val)
    city_obj.save()

    return jsonify(city_obj.to_dict()), 200
