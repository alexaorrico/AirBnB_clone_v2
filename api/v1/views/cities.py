#!/usr/bin/python3
"""Handles all RESTful API actions for City objects"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=['GET'])
def cities_by_state(state_id):
    """Retrieve the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=['GET'])
def get_city(city_id):
    """Retrieve a City object by its ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    return jsonify(city.to_dict())


@app_views.route("/states/<state_id>/cities", methods=['POST'])
def create_city(state_id):
    """Create a new City object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    city = City(**data)
    city.state_id = state_id
    city.save()

    return jsonify(city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=['PUT'])
def update_city(city_id):
    """Update a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """Delete a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    
    city.delete()
    storage.save()

    return jsonify({}), 200
