#!/usr/bin/python3
'''BLueprint implementation for city model'''

from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
import os


@app_views.route('cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_cities(city_id=None):
    '''Return the list of all City objects'''
    if request.method == 'DELETE':
        return del_city(city_id)
    elif request.method == 'PUT':
        return update_city(city_id)
    elif request.method == 'GET':
        return get_cities(city_id)


@app_views.route('states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_state_cities(state_id):
    '''Hadnles direction to actual view function'''
    if request.method == 'POST':
        return add_city(state_id)
    elif request.method == 'GET':
        return get_state_cities(state_id)


def get_state_cities(state_id):
    '''Return all citie linked to a state'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        cities = state.cities()
    else:
        cities = list(state.cities)
    return jsonify([city.to_dict() for city in cities])


def get_cities(city_id):
    '''Reurn a city given an id'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


def del_city(city_id):
    '''Deletes a city obj with city_id'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


def add_city(state_id):
    '''Adds city to cities'''
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    if 'name' not in req_data:
        abort(400, 'Missing name')
    city = City(**req_data)
    city.state_id = state.id
    city.save()
    return get_cities(city.id), 201


def update_city(city_id):
    '''Update a city instance'''
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    try:
        req_data = request.get_json()
    except Exception:
        abort(400, 'Not a JSON')
    if type(req_data) is not dict:
        abort(400, 'Not a JSON')
    for key, val in req_data.items():
        if key != 'id' or key != 'created_at' or key != 'updated_at':
            setattr(city, key, val)
    city.save()
    return get_cities(city.id), 200
