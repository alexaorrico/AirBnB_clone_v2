#!/usr/bin/python3
"""Module for City views"""
from flask import jsonify, abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_list_cities(state_id):
    """Retrieves the list of all cities of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete city with its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a city and returns the new city with status code 201"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()

    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    if "name" not in data:
        return make_response("Missing name", 400)

    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a city and returns the city with status code 200"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None or type(data) != dict:
        return make_response("Not a JSON", 400)

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
