#!/usr/bin/python3
'''
    City route for the API
'''
from flask import Flask
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities(state_id):
    state = storage.get(State, state_id)
    """get city information for all states"""
    if not str(state_id) in str(storage.all(State)):
        abort(404)
    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)

@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """get city information for specific states"""
    city = storage.get(City, city_id)
    if city != None:
        return jsonify(city.to_dict())
    else:
        abort(404)

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city based on its city_id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return {}

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ create a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    createJson = request.get_json()
    if createJson is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if not 'name' in createJson.keys():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    city = City(**createJson)
    city.state_id = state_id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr != 'id' or attr != 'created_at' or attr != 'updated_at':
            setattr(city, attr, val)
    storage.save()
    return jsonify(city.to_dict()), 200
