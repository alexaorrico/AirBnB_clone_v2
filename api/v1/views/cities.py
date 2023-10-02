#!/usr/bin/python3
"""
New view for City objects that handles all default RESTFul API actions
"""
from flask import Flask, request, jsonify, abort
from api.v1.views import app_views
from models import storage, State, City

# Route to retrieve a list of all City objects of a State
@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """get a list of all city objects of a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)

# Route to retrieve a specific City object by city_id
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """get a specific city object by city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

# Route to delete a specific City object by city_id
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete a specific city object by city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

# Route to create a new City object for a State
@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a new city object for a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    
    new_city = City(**data)
    new_city.state_id = state_id
    new_city.save()
    
    return jsonify(new_city.to_dict()), 201

# Route to update a specific City object by city_id
@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a specific city object by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    
    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")
    
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    
    city.save()
    
    return jsonify(city.to_dict()), 200
