#!/usr/bin/python3
"""Handles all default RESTful API actions for City objects"""

from models import storage
from models.city import City
from models.state import State
from flask import abort, jsonify, request
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False, endpoint='get_all')
def get_all_cities_in_state(state_id):
    """Returns a JSON list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    list_of_cities = [city.to_dict() for city in state.cities]

    return jsonify(list_of_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False, endpoint='get_city')
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False, endpoint='delete_city')
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False, endpoint='create_city')
def create_city(state_id):
    """Creates a City"""
    if storage.get(State, state_id) is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    name = json_data.get('name')
    if name is None:
        abort(400, description='Missing name')

    json_data['state_id'] = state_id  # adds the state_id attribute

    # sends complete json_data to be used to create the City object
    new_city = City(**json_data)

    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False, endpoint='update_city')
def update_city(city_id):
    """Updates a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()

    for key, value in json_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)

    city.save()

    return jsonify(city.to_dict()), 200
