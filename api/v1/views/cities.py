#!/usr/bin/python3

from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def handle_cities(state_id):
    if request.method == 'GET':
        return get_cities(state_id)
    elif request.method == 'POST':
        return add_city(state_id)

@app_views.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_city(city_id):
    if request.method == 'GET':
        return get_city(city_id)
    elif request.method == 'PUT':
        return update_city(city_id)
    elif request.method == 'DELETE':
        return del_city(city_id)

def get_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        raise NotFound("State not found")
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities), 200

def get_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        raise NotFound("City not found")
    return jsonify(city.to_dict()), 200

def add_city(state_id):
    state = storage.get(State, state_id)
    if not state:
        raise NotFound("State not found")
    data = request.get_json()
    if not data:
        raise BadRequest("Not a JSON")
    if 'name' not in data:
        raise BadRequest("Missing name")
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201

def update_city(city_id):
    city = storage.get(City, city_id)

    if not city:
        raise NotFound("City not found")
    data = request.get_json()
    if not data:
        raise BadRequest("Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
        storage.save()
        return jsonify(city.to_dict()), 200

def del_city(city_id):
    city = storage.get(City, city_id)
    if not city:
        raise NotFound("City not found")
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
