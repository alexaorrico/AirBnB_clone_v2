#!/usr/bin/python3
""" Script for the city views """
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities_by_states(state_id=None):
    requested_state = storage.get(State, state_id)
    if not requested_state:
        abort(404)
    cities = []
    requested_city = requested_state.cities
    for city in requested_city:
        cities.append(city.to_dict())
    return jsonfy(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_cityid(city_id=None):
    requested_city = storage.get(City, city_id)
    if not requested_city:
        abort(404)
    return jsonfy(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ delete a city and if no city found retunrs 404 error """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id=None):
    """ Creates a City: POST /api/v1/states/<state_id>/citie """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    city = City(name=request.json['name'], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
