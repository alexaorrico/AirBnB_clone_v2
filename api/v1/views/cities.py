#!/usr/bin/python3
""" module view for city objects;
handles all default Restful API actions
"""
from flask import Flask, jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from . import app_views
import uuid


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities_by_states(state_id):
    """gets list of all state objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = state.cities
    citiess = [city.to_dict() for city in cities]
    return jsonify(citiess)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id=None):
    """get city by id"""

    # print("Full request: ", request)
    city = storage.get(City, city_id)
    # print('State id is {}'.format(state_id))
    # print('State id is type {}'.format(type(state_id)))
    # print('State is {}'.format(state))

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a city identified by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """create city from http request"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state.id
    city = City(**data)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, val in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, val)
    city.save()
    return jsonify(city.to_dict()), 200
