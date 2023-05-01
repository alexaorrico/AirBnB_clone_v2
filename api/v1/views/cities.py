#!/usr/bin/python3
"""
Handle all default RESTFUL API actions
"""
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import Flask, request, abort, jsonify
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def cities_in_state(state_id):
    """ Returns all cities in a state id"""
    my_state = storage.get('State', state_id)
    if my_state is None:
        abort(404)
    cities = []
    for city in my_state.cities:
        cities.append(city.to_dict())
    if request.method == 'GET':
        return jsonify(cities)
    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, 'Not a JSON')
        if 'name' not in data:
            abort(400, 'Missing name')
        data['state_id'] = state_id
        new_city = City(**data)
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def city(city_id):
    """ Returns city object of id """
    city = storage.get('City', city_id)
    if city is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(city.to_dict())
    elif request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, 'Not a JSON')
        for k, v in data.items():
            ign_attr = ['id', 'created_at', 'updated_at']
            if k not in ign_attr:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200

    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
