#!/usr/bin/python3
""" Routes for State responses """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, state, city
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=["GET"],
                 strict_slashes=False)
def all_cities(state_id=None):
    """retrieves a list of all cities by state id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_list = [city.to_dict() for city in cities]
    return (jsonify(cities_list), 200)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def specific_city(city_id=None):
    """Get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city by ID """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """ Creates new city """
    req = request.get_json()
    if req is False:
        abort(400, "Not a JSON")
    name = req.get("name")
    if "name" not in req:
        abort(400, "Missing name")
    if storage.get(State, state_id) is None:
        abort(404)
    new_city = City()
    new_city.state_id = state_id
    new_city.name = name
    new_city.save()
    return (jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """ Update a city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key in ['id', 'created_at', 'updated_at']:
            continue
        else:
            setattr(city, key, value)
    city.save()
    return (jsonify(city.to_dict()), 200)
