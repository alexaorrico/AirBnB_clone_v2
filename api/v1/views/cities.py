#!/usr/bin/python3
""" Objects that handle default RESTFUL API actions for cities """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request

@app_views.route('/states/<state_id>/cities', methods=['GET'],strict_slashes=False)
def get_cities_by_state(state_id):
    """ Retrieves a list of all City objects of a State"""
    state = storage.get(State, state_id)
    list_cities = []
    if not state:
        abort(404)

    for city in state.cities:
        list_cities.append(city.to_dict())
    
    return jsonify(list_cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a specific city based on id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """ Creates a new city object """
    state = storage.get_state(State, state_id)
    if not state: 
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    
    data = request.get_json()
    instance  = City(**data)
    instance.state_id = state_id
    instance.save()
    return jsonify(instance.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    
    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict(), 200)
