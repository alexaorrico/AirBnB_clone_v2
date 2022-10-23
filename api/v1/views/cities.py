#!/usr/bin/python3
"""This module handles city routes"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views

from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def cities_route(state_id):
    """
    cities_route handles get, post request to cities
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = list(map(lambda city: city.to_dict(), state.cities))
        return make_response(jsonify(cities), 200)
    elif request.method == 'POST':
        req_data = request.get_json(silent=True)
        if req_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in req_data:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        new_city = City(**req_data, state_id=state_id)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def city_route(city_id):
    """
    city route handles get, put and delete to a specific city
    """

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(city.to_dict()), 200)
    elif request.method == 'DELETE':
        city.delete()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        req_data = request.get_json(silent=True)
        if req_data is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        city.update(**req_data)
        return make_response(jsonify(city.to_dict()), 200)
