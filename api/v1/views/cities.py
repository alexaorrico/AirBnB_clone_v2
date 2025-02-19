#!/usr/bin/python3
""" API endpoints for cities """

from models import storage
from models.state import State
from models.city import City

from flask import jsonify, abort, request

from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'])
def get_cities(state_id):
    """ Gets the list of all cities of a state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>',
                 methods=['GET'])
def get_city(city_id):
    """ Gets a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'])
def delete_city(city_id):
    """ Deletes a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'])
def create_city(state_id):
    """ Creates a city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'])
def update_city(city_id):
    """ Updates a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    forbidden_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
