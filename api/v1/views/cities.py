#!/usr/bin/python3
""" new view for Cities objects """

from models.city import City
from models.state import State
from flask import Flask, jsonify, request
from api.v1.views import app_views
from models import storage, base_model


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['GET']
)
def get_cities(state_id):
    """Retrieves the list of all Cities objects"""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    else:
        cities_list = []
        for city in state.cities:
            cities_list.append(city.to_dict())
        return jsonify(cities_list)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Get city by its id"""
    city_id = storage.get(City, city_id)
    if city_id is None:
        return abort(404)
    return jsonify(city_id.to_dict())


@app_views.route(
    '/cities/<city_id>',
    strict_slashes=False,
    methods=['DELETE']
)
def delete_city_ob(city_id):
    """Delete a City object by id"""
    city_id = storage.get(City, city_id)
    if city_id is None:
        return abort(404)
    else:
        storage.delete(city_id)
        storage.save()
        return jsonify({}), 200


@app_views.route(
    '/states/<state_id>/cities',
    strict_slashes=False,
    methods=['POST']
)
def create_city_ob(state_id):
    """Creates a City"""
    if request.method == 'POST':
        state = storage.get(State, state_id)
        test = request.get_json()
        if not state:
            return abort(404)
        if not test:
            return "Not a JSON", 400
        elif "name" not in test:
            return "Missing name", 400
        else:
            ob = City(**test)
            ob.state_id = state_id
            storage.new(ob)
            storage.save()
            return jsonify(ob.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city_ob(city_id):
    """Update a User object"""
    if request.method == 'PUT':
        ob = storage.get(User, city_id)
        data = request.get_json()
        if not ob:
            return abort(404)
        if not data:
            return "Not a JSON", 400
        for key, val in data.items():
            if key not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(ob, key, val)
        storage.save()
        return jsonify(ob.to_dict()), 200
