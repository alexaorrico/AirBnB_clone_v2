#!/usr/bin/python3
"""
Create the logic for the cities endpoint
"""
from models import storage
from models.city import City
from . import app_views

from flask import abort, make_response, jsonify, request


@app_views.route('states/<state_id>/cities', methods=['GET'])
def cities_list(state_id):
    """get a list of cities of a particular state id
    """
    all_states = storage.all('State')
    found_list = []
    for state in all_states.values():
        if state.id == state_id:
            for city in state.cities:
                found_list.append(city.to_dict())
            return found_list
    if len(found_list) == 0:
        abort(404)


@app_views.route('cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """get a city instance with id of city_id
    """
    all_cities = storage.all('City')
    for city in all_cities.values():
        if city.id == city_id:
            return jsonify(city.to_dict())
    abort(404)


@app_views.route('cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a city with id of city_id from storage
    """
    all_cities = storage.all('City')
    for city in all_cities.values():
        if city.id == city_id:
            storage.delete(city)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a new city in state with id state_id
    """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    request_body = request.get_json()
    if 'name' not in request_body.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    for state in storage.all('State').values():
        if state.id == state_id:
            new_city = City(**request_body)
            new_city.state_id = state.id
            storage.new(new_city)
            storage.save()
            return make_response(jsonify(new_city.to_dict()), 201)
    abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update an existing city instance with new info
    """
    if not request.json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    request_body = request.get_json()
    all_cities = storage.all('City')
    for city in all_cities.values():
        if city.id == city_id:
            for key, val in request_body.items():
                if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                    city.key = val
            return make_response(jsonify(city.to_dict()), 200)

    abort(404)
