#!/usr/bin/python3

""" Module for cities
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities_by_state(state_id):
    """
    Return cities by state with the id
    """
    list_city = []
    state = storage.get("State", state_id)
    if state is not None:
        for city in state.cities:
            list_city.append(city.to_dict())
        return jsonify(list_city)
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>')
def cities_by_id(city_id):
    """
    Return cities by id
    """
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def del_city(city_id):
    """
    Delete a city by id
    """
    city = storage.get("City", city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return jsonify({})
    return jsonify({"error": "Not found"}), 404


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['POST'])
def create_city(state_id):
    """
    Create a new object city
    """
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": 'Missing name'}), 400)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    city = request.get_json()
    city['state_id'] = state_id
    new_city = City(**city)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Update a city by id
    """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": 'Not a JSON'}), 400)
    params = request.get_json()
    skip = ['id', 'created_at', 'updated_at']
    for key, value in params.items():
        if key not in skip:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict())


@app_views.errorhandler(404)
def page_not_found(error):
    """
    Handle 404 error
    """
    return jsonify({"error": "Not found"}), 404
