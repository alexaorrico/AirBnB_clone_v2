#!/usr/bin/python3
"""
Methods for City class in our API
"""
from models.state import State
from models.city import City
from models import storage
import json
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                strict_slashes=False)
def get_city_by_state(state_id):
    """Method to get al cities by state id"""
    states = storage.all(State)
    cities = storage.all(City)
    cities_in_state = []
    for state in states.values():
        if state.id == state_id:
            for city in cities.values():
                if city.stateId == state_id:
                    cities_in_state.append(city.to_dict())
            return jsonify(cities_in_state)
    abort(404)
    return


@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Get a single city by id number"""
    cities = storage.all(City)
    for city in cities.values():
        if city.id == city_id:
            return(jsonify(city.todict()))
    abort(404)
    return


@app_views.route('cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """deletes a single city"""
    cities = storage.all(City)

    for city in city.values():
        if city.id == city_id:
            city.delete()
            storage.save()
            return jsonify({}), 200
    abort(404)

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a new city"""
    payload = request.get_json(silent=True)
    states = storage.all(State)

    if payload is None:
        abort(400, 'Not a JSON')
    elif 'name' not in payload:
        abort(400, 'Missing name')

    for state in states.values():
        if state.id == state_id:
            new_city = City(**payload)
            setattr(new_city, 'state_id', state_id)
            new_city.save()
            return(jsonify(new_city.to_dict()), 201)
    abort(404)
    return


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Method to update a city object"""
    payload = request.get_json(silent=True)
    cities = storage.all(City)

    if payload is None:
        abort(400, 'Not a JSON')

    for city in cities.values():
        if city.id == city_id:
            for k, v in payload.items():
                if k != 'created_at' and k != 'updated_at' and k != 'id':
                    setattr(city, k, v)
            return(jsonify(city.to_dict()), 200)
    abort(404)
