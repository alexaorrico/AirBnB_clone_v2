#!/usr/bin/python3
"""
View for Cities that handles all RESTful API actions
"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def cities_all(state_id):
    """Returns a list of all City objects of a given state"""
    cities = storage.all(City).values()
    state_cities = []
    for city in cities:
        if city.state_id == state_id:
            state_cities.append(city.to_dict())
    return jsonify(state_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Returns a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city = city.to_dict()
    return jsonify(city)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """"Deletes a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Adds a new city"""
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    city = city.to_dict()
    return jsonify(city), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        special_keys = ['id', 'created_at', 'updated_at']
        if key not in special_keys:
            setattr(city, key, value)
        city.save()
        city = city.to_dict()
        return jsonify(city), 200
