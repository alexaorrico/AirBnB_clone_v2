#!/usr/bin/python3
"""Create a new view for City Objects."""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_all_cities(state_id):
    """Returns all cities by state id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])

@app_views.route('/cities/<city_id>', methods['GET'])
def get_city(city_id):
    """Retrieves a city object by city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a city object by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new city object by state ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    if "name" not in json_data:
        abort(400, "Missing name")
    new_city = City(name=json_data["name"], state_id=state_id)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Updates an existing City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")

    ignored_keys = {"id", "state_id", "created_at", "updated_at"}
    for key, value in json_data.items():
        if key not in ignored_keys:
            setattr(city, key, value)

    storage.save()

    return jsonify(city.to_dict()), 200
