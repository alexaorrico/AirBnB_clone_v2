#!/usr/bin/python3
"""cities views"""
from models.city import City
from flask import abort, request, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def retrives_all_cities(state_id):
    """Retrives the list of all cities"""
    if storage.get(State, state_id) is None:
        abort(404)
    state = storage.get(State, state_id)
    return jsonify([
        city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'])
def retrives_city(city_id):
    """Retrives a city from id"""
    if storage.get(City, city_id) is None:
        abort(404)
    return jsonify(storage.get(City, city_id).to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """creates a new city"""
    if storage.get(State, state_id) is None:
        abort(404)
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    if 'name' not in json_data:
        abort(400, 'Missing name')
    city = City(**json_data)
    setattr(city, 'state_id', state_id)
    city.save()
    # return a tuple default(data, status)
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city"""
    json_data = request.get_json()
    if json_data is None:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, values in json_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'state_id'):
            setattr(city, key, values)
    city.save()
    return jsonify(city.to_dict()), 200
