#!/usr/bin/python3
""" default Restful API actions """
from flask import jsonify, abort, request
from models.state import State
from api.v1.views import app_views
from api.v1.views.cities import *


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """ get storage from state and cities """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ To retrieve a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app.route('/api/v1/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ To delete a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app.route('/api/v1/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ To create a City object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    city = City(**request.json)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app.route('/api/v1/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ To update a City object """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200

