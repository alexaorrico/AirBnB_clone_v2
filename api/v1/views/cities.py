#!/usr/bin/python3
"""
    a view for City objects that handles all default RESTFul API actions:
"""

from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """t
        his will retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    if cities is None:
        abort(404)
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """
        will retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def city_del(city_id):
    """
        this will delete a City object if found
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def city_add(state_id):
    """
        this will create a new City by using state_id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    add_city = City(**data)
    add_city.save()
    return jsonify(add_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def city_update(city_id):
    """
        this will update a City object by ID.
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')

    keystopass = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in keystopass:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())
