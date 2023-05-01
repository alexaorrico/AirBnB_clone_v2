#!/usr/bin/python3
"""View for City objects"""
from flask import Flask, jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_all_cities(state_id):
    """retrieves list of all City objects of State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = state.cities
    cities_dict = []
    for city in cities:
        cities_dict.append(city.to_dict())
    return jsonify(cities_dict)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """return JSON of city with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """deletes a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def add_city(state_id):
    """ creates a new City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in req_json:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    req_json["state_id"] = state_id
    new_city = City(**req_json)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201
    
@app_views.route("/cities/<cities_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """updates a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_json = request.get_json()
    if not req_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
     
    for key, value in req_json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
