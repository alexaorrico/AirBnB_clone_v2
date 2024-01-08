#!/usr/bin/python3
"""Defines API routes and CRUD operations for City resource within a State"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


# Route to list all cities of a state
@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    '''Retrieves a list of all City objects of a given State'''
    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)

    list_cities = [obj.to_dict() for obj in storage.all("City").values()
                   if state_id == obj.state_id]
    return jsonify(list_cities)


# Route to create a new city in a state
@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a new City within a given State'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')

    all_states = storage.all("State").values()
    state_obj = [obj.to_dict() for obj in all_states if obj.id == state_id]
    if state_obj == []:
        abort(404)

    cities = []
    new_city = City(name=request.json['name'], state_id=state_id)
    storage.new(new_city)
    storage.save()
    cities.append(new_city.to_dict())
    return jsonify(cities[0]), 201


# Route to retrieve information about a specific city
@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Retrieves information about a specific City'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    return jsonify(city_obj[0])


# Route to delete a city
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a specific City'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)

    city_obj.remove(city_obj[0])
    for obj in all_cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


# Route to update information about a city
@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    '''Updates information about a specific City'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    city_obj[0]['name'] = request.json['name']
    for obj in all_cities:
        if obj.id == city_id:
            obj.name = request.json['name']

    storage.save()
    return jsonify(city_obj[0]), 200
