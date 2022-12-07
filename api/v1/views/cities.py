#!/usr/bin/python3
"""Views for the City class: GET, DELETE,  POST, PUT"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities_from_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    objs = []
    for x in state.cities:
        objs.append(x.to_dict())
    return jsonify(objs)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    d = request.get_json()
    d.update({"state_id": state_id})
    obj = City(**request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city.__dict__.update(request.get_json())
    old_dict = city.to_dict()
    storage.delete(city)
    city = City(**old_dict)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 200
