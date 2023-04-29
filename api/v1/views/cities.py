#!/usr/bin/python3
"""Handles all RESTFul API actions for City"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Returns a list of all City Objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([x.to_dict() for x in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Returns a City Object with a matching id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes the City object with the matching id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new City object for a matching state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    elif 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    city = City(name=data['name'], state_id=state.id)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates matching City Object with JSON data"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    for key in ['id', 'state_id', 'created_at', 'updated_at']:
        try:
            data.pop(key)
        except KeyError:
            pass

    for key, value in data.items():
        setattr(city, key, value)

    storage.save()
    return jsonify(city.to_dict()), 200
