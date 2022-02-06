#!/usr/bin/python3
"""cities routes"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def all_city(state_id):
    """list all cities by state"""
    state = (storage.get('State', state_id))
    city = state.cities
    if city:
        return jsonify([value.to_dict() for value in city]), 200
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_id(city_id):
    """json data of a single city"""
    city = (storage.get('City', city_id))
    if city:
        return jsonify(city.to_dict()), 200
    abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """delete json data of a single city"""
    city = (storage.get('City', city_id))
    if city:
        city.delete()
        storage.save()
        return {}, 200
    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def creat_city(state_id):
    """create a new city"""
    dictionary = request.get_json()
    states = (storage.get('State', state_id))
    if states is None:
        abort(404)
    if dictionary is None:
        abort(400, 'Not a JSON')
    if dictionary.get('name') is None:
        abort(400, 'Missing name')
    city = City()
    city.name = dictionary.get('name')
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update(city_id):
    """Update data of city"""
    dictionary = request.get_json()
    city = (storage.get('City', city_id))
    if city is None:
        abort(404)
    if dictionary is None:
        abort(400, 'Not a JSON')
    [setattr(city, key, value) for key, value in dictionary.items()
     if key not in ['id', 'state_id', 'created_at', 'updated_at']]
    city.save()
    return jsonify(city.to_dict()), 200
