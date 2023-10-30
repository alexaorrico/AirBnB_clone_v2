#!/usr/bin/python3
"""
 view for City objects that handles all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False)
def get_city_state(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = state.cities
    cities_serializable = []
    for city in all_cities:
        cities_serializable.append(city.to_dict())
    return jsonify(cities_serializable)


@app_views.route('/cities/<city_id>',
                 strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """
    Creates a City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    if 'name' not in content:
        abort(400, 'Missing name')
    city = City(**content)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """
    Updates a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    content = request.get_json()
    if content is None:
        abort(400, 'Not a JSON')
    skip = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in content.items():
        if key not in skip:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
