#!/usr/bin/python3
from flask import abort, jsonify, request
from models import City, State
from api.v1.views import app_views

#Retrive handle
@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    state = State.get(state_id)
    if not state:
        abort(404)
    cities = City.filter_by(state_id=state_id)
    return jsonify([city.to_dict() for city in cities])

#Retrieve handle
@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

#Delete handle
@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    city.delete()
    return jsonify({}), 200

#Create handle
@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    state = State.get(state_id)
    if not state:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')
    city = City()
    city.state_id = state_id
    city.name = data['name']
    city.save()
    return jsonify(city.to_dict()), 201

#Update handle
@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city = City.get(city_id)
    if not city:
        abort(404)
    if not request.is_json:
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignored_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
