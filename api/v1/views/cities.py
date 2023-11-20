#!/usr/bin/python3
"""
View for State objects that will handle all default
RESTful API actions
"""
# Allison Edited 11/20 3:45 PM
from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """retrieves the list of all city objects based off of state id"""
    city_list = []
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        city_list.append(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """retrieves a city object when a specific city_id is provided
        will return 404 error if city is not found."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """deletes city object specified by city_id, returns a 404 error
        if city is not found, returns empty dictionary with status code 200"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def new_city(state_id):
    """Creates a new city for state based off of state id provided
    transforms the HTTP body request to a dictionary
    handles error raises, returns new state with status code 201"""

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json:
        abort(400, description="Missing name")

    new_info = request.get_json()
    city = City(**new_info)
    """** -> double asterisks unpacks a dictionary and passes
    the key-value pairs as arguments to the state constructor!"""
    city.state_id = state.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_the_city(city_id):
    """updates a city based off of city id given in request, returns the
    city object and status code 200"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    key_ignore = ['id', 'created_at', 'updated_at']

    new_data = request.get_json()
    for key, value in new_data.items():
        if key not in key_ignore:
            setattr(city, key, value)

    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
