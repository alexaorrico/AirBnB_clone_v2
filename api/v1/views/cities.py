#!/usr/bin/python3
"""Module to create a new view for State objects"""

from flask import jsonify, Flask, request
from models import storage
from api.v1.views import app_views
from models.state import State
from models.city import City

@app_views.route('states/<state_id>/cities', methods=['GET'],
                 strict_slashes = False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State by state_id"""
    city = storage.get('City', str(state_id))
    if State is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())

@app_views.route('cities/<city_id>', methods=['GET'],
                 strict_slashes = False)
def get_cities(city_id):
    """Retrieves the list of all City objects of a State by state_id"""
    city = storage.get('City', str(city_id))
    if City is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes = False)
def delete_city_by_id(city_id):
    """Deletes a state by ID"""
    state = storage.get('City', city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(city)
    storage.all('City').pop("{}.{}".format('City', city_id))
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes = False)
def create_city(state_id):
    """Post a City object"""
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    if 'name' not in data:
        abort(400)
        abort(Response("Missing name"))
    new_city = City(**data)
    return jsonify(new_city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes = False)
def put_city(city_id):
    """Put a City object"""
    data = request.get_json()
    if not data:
        abort(400)
        abort(Response("Not a JSON"))
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 200
