#!/usr/bin/python3
"""view for Cities objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route('states/<state_id>/cities', strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all City given an State"""
    cities_list = []
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_by_id(city_id):
    """Retrieves a city by a given ID"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
    )
def create_city(state_id):
    """Creates a City object"""
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request_data:
        return jsonify({"error": "Missing name"}), 400
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    request_data['state_id'] = state_id
    obj = City(**request_data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "Not a JSON"}), 400
    for k, v in request_data.items():
        setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
