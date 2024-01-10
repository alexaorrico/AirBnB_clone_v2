#!/usr/bin/python3

from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models import *

@app_views.route('/states/<state_id>/cities', methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    """get all cities of state objects"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """retrieve city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """method to delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """creates new object city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@app_views.route('cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update city by id"""
    city =  storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
