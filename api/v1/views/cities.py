#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@swag_from('documentation/cities_by_state.yml', methods=['GET', 'POST'])
def get_cities_by_state(state_id=None):
    """
    This function handles HTTP methods for cities in a given state.
    """
    state = storage.get('State', state_id)
    if state is None:
        abort(404)

    if request.method == 'GET':
        all_cities = storage.all('City')
        state_cities = [city.to_json() for city in all_cities.values()
                        if city.state_id == state_id]
        return jsonify(state_cities)

    if request.method == 'POST':
        req_json = request.get_json()
        if not req_json or 'name' not in req_json:
            abort(400)
        city_class = CNC.get('City')
        req_json['state_id'] = state_id
        new_city = city_class(**req_json)
        new_city.save()
        return jsonify(new_city.to_json()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('documentation/cities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def get_city(city_id=None):
    """
    This function handles HTTP methods for a single city.
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_json())

    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if not req_json:
            abort(400)
        city.bm_update(req_json)
        storage.save()
        return jsonify(city.to_json()), 200
