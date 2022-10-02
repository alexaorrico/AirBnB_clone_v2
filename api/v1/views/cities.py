#!/usr/bin/python3
"""Module with the view for City objects"""
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage
from flask import request, abort, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities(state_id):
    """Return a list of dictionaries of all cities of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        cities = []
        for city in state.cities:
            cities.append(city.to_dict())
        return jsonify(cities)
    data = request.get_json()
    if data is None:
        return 'Not a JSON', 400
    if 'name' not in data.keys():
        return 'Missing name', 400
    data['state_id'] = state_id
    new_city = City(**data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_city(city_id):
    """Get a City instance from the storage"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return 'Not a JSON', 400
        for k, v in data.items():
            if k != 'id' or k != 'state_id' or k != 'created_at'\
               or k != 'updated_at':
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
