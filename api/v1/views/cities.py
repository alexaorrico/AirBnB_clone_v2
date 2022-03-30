#!/usr/bin/python3
"""
create a new view for City objects that handles
all default RESTFul API actions
"""
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import abort
from flask import request
from flask.json import jsonify

@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_from_state(state_id=None):
    """
    retrieves list of cities in a state
    """
    all_states = storage.all(State)
    info = []
    if all_states is not {} and state_id is not None:
        for state in all_states.values():
            if state.id == state_id:
                for city in state.cities:
                    info.append(city.to_dict())
                return jsonify(info)
    abort(404)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_cities(city_id=None):
    """
    gets city by city_id
    """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """
    deletes a city
    """
    city = storage.get(City, city_id)
    if city is not None:
        city.delete()
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/states/<state_id>/cities', strict_slashes=False, methods=['POST'])
def create_city(state_id=None):
    """
    creates a new city
    """
    json = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if json is None:
        abort(400, "Not a JSON")
    if 'name' not in json:
        abort(400, "Missing name")
    city = City(**json)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """
    Updates a City
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json = request.get_json(silent=True)
    if json is None:
        abort(400, "Not a JSON")
    for key, value in json.items():
        if key != "updated_at" and key != "created_at" and key != "state_id" and key != "id":
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
