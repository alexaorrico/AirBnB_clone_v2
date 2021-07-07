#!/usr/bin/python3
"""cities Module"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all cities in a state objects"""
    state = storage.get(State, state_id)
    cities_list = []
    if state is None:
        abort(404)
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_by_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City in a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    if 'name' not in request_dict:
        abort(400, 'Missing name')
    city = City(**request_dict)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    request_dict = request.get_json()
    if request_dict is None:
        abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for key, value in request_dict.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
