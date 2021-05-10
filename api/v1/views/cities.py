#!/usr/bin/python3
"""
Flask route that returns status of state JSON object response in app_views
"""
from api.v1.views import app_views
from flask import Flask, jsonify, make_response, request, abort
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_from_state(state_id=None):
    """cities not linked to an object
    """
    # Checks if state exists / retrieves the state object requested by ID
    given_state = storage.get('State', state_id)
    if given_state is None:
        abort(404, 'Not found')
    # ===================================================================
    # returns json representation of all cities in given state
    if request.method == 'GET':
        all_cities = [city.to_dict() for city
                      in given_state.cities]
        return jsonify(all_cities)
    # ====================================================================
    if request.method == 'POST':
        json_req = request.get_json()
        if not json_req:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in json_req:
            return make_response(jsonify({'error': 'Missing name'}), 400)
        city = City(**json_req)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_cities(city_id=None):
    # Checks if city exists / retrieves the city object requested by ID
    given_city = storage.get('City', city_id)
    if given_city is None:
        abort(404, 'Not found')
    # =================================================================
    if request.method == 'GET':
        return jsonify(given_city.to_dict())
    if request.method == 'DELETE':
        given_city.delete()
        storage.save()
        return (jsonify({}), 200)
    if request.method == 'PUT':
        if request.get_json() is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in request.get_json().items():
            if attr not in ['id', 'created_at', 'updated_at']:
                setattr(given_city, attr, value)
    given_city.save()
    return jsonify(given_city.to_dict())
