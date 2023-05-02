#!/usr/bin/env python3
"""Defines all api for cities"""
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def cities(state_id):
    """Retrive list of cities in a particular state"""
    states = storage.get("State", state_id)
    if states == "None":
        abort(404)
    cities = states.cities
    return jsonify([city.to_dict() for city in cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city(city_id):
    """Retrive a city with a particular id from database"""
    city = storage.get(City, city_id)
    if city == "None":
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city from the data base"""
    city = storage.get(City, city_id)
    if city == "None":
        abort(404)
    print(city.to_dict())
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a new city in a state"""
    city = request.get_json()
    state = storage.get(State, state_id)
    if state == "None":
        abort(404)
    if not city:
        abort(404, "Not a JSON")
    if "name" not in city:
        abort(404, "Missing name")
    new_city = City(**city)
    setattr(new_city, 'state_id', state_id)
    storage.new(new_city)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"],
                 strict_slashes=False)
def update_city(city_id):
    """Update a city by its id"""
    city = storage.get(City, city_id)
    data = request.get_json()
    print(data)
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
