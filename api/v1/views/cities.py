#!/usr/bin/python3

"""City management endpoints"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    '''Fetches all City objects associated with a specific State'''
    states_collection = storage.all("State").values()
    state_details = [state.to_dict() for state in states_collection \
       if state.id == state_id]
    if not state_details:
        abort(404)
    cities_collection = [city.to_dict() for city in \
       storage.all("City").values() if city.state_id == state_id]
    return jsonify(cities_collection)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a new City object under a specific State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states_collection = storage.all("State").values()
    state_details = [state.to_dict() for state in states_collection \
       if state.id == state_id]
    if not state_details:
        abort(404)
    cities_list = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities_list.append(new_city.to_dict())
    return jsonify(cities_list[0]), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Fetches a specific City object by ID'''
    cities_collection = storage.all("City").values()
    city_details = [city.to_dict() for city in cities_collection if \
       city.id == city_id]
    if not city_details:
        abort(404)
    return jsonify(city_details[0])


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a specific City object by ID'''
    cities_collection = storage.all("City").values()
    city_details = [city.to_dict() for city in cities_collection if \
       city.id == city_id]
    if not city_details:
        abort(404)
    city_details.remove(city_details[0])
    for city in cities_collection:
        if city.id == city_id:
            storage.delete(city)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    '''Updates an existing City object'''
    cities_collection = storage.all("City").values()
    city_details = [city.to_dict() for city in cities_collection if \
       city.id == city_id]
    if not city_details:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_details[0]['name'] = request.json['name']
    for city in cities_collection:
        if city.id == city_id:
            city.name = request.json['name']
    storage.save()
    return jsonify(city_details[0]), 200
