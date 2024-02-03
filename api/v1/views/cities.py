#!/usr/bin/python3
""""Cities views"""
from flask import abort, request, jsonify

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_of_state(state_id):
    "Get a list of all cities of a state"
    state = storage.get(State, state_id)
    if state:
        return jsonify([city.to_dict() for city in state.cities])

    abort(404)


@app_views.route('/cities/<id>', methods=['GET'])
def city_by_id(id):
    "Get a city by ID"
    city = storage.get(City, id)
    if city:
        return city.to_dict()

    abort(404)


@app_views.route('/cities/<id>', methods=['DELETE'])
def delete_city(id):
    "Delete the city with ID"
    city = storage.get(City, id)
    if city:
        storage.delete(city)
        storage.save()
        return {}

    abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    "Create a new city"
    if not storage.get(State, state_id):
        abort(404)
    if not request.is_json:
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data.get('name'):
        abort(400, 'Missing name')
    new_city = City(state_id=state_id, **data)
    new_city.save()
    return new_city.to_dict(), 201


@app_views.route('/cities/<id>', methods=['PUT'])
def update_city(id):
	city = storage.get(City, id)
	if not city:
		abort(404)
	if not request.is_json:
		abort(400, 'Not a JSON')
	data = request.get_json()
	for k, v in data.items():
		if k not in ['id', 'state_is', 'created_at', 'updated_id']:
			setattr(city, k, v)
	city.save()
	return city.to_dict()

