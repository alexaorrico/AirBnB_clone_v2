#!/usr/bin/python3
""" cities main file """

from flask import request, jsonify, abort, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """
    all cities with state_id
    """
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    list_cities = [city.to_dict() for city in state.cities]

    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """
    get city by id
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    delete city by id
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Create a new city
    """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    new_data = request.get_json()
    new_city = City(**new_data)
    new_city.state_id = state.id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    Update a city
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    new_data = request.get_json()
    for key, value in new_data.items():
        setattr(city, key, value)

    city.save()

    return make_response(jsonify(city.to_dict()), 200)