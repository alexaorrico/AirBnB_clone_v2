#!/usr/bin/python3
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from api.v1.app import not_found
from flask import jsonify
from flask import request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return not_found("State not found")
    cities = storage.all(City)
    filtered_cities = []
    for key, val in cities.items():
        new = {}
        new[key] = val.to_dict()
        if (new[key])["state_id"] == state_id:
            filtered_cities.append(new)
    return jsonify(filtered_cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return not_found("City not found")
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    obj = storage.get(City, city_id)
    if obj is None:
        return not_found("City not found")
    obj.delete()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city_in_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        return not_found("State not found")
    req = request.get_json()
    if not isinstance(req, dict):
        return jsonify("Not a JSON"), 400
    if "name" not in req.keys():
        return jsonify("Missing name"), 400
    new_city = City()
    new_city.state_id = state_id
    new_city.name = req['name']
    return jsonify(new_city.to_dict()), 201


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT']
)
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        return not_found("City not found")
    req = request.get_json()
    if not isinstance(req, dict):
        return jsonify("Not a JSON"), 400
    for key, val in req.items():
        setattr(city, key, val)
    return jsonify(city), 200
