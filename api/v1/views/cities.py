#!/usr/bin/python3
""" Handles Restful API actions for Cities """
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns City object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_in_state(state_id):
    """Returns all Cities in the State that matches the ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes City with the given ID"""

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city_in_state(state_id):
    """
    Creates a new City in State that matches ID
    """
    if not request.json:
        abort(400, "Not a JSON")

    data = request.json
    if 'name' not in data.keys():
        abort(400, "Missing name")

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()

    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object that matches ID"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    titles_ignore = ['id', 'created_at', 'updated_at']

    city_info = request.get_json()
    for key, value in city_info.items():
        if key not in titles_ignore:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
