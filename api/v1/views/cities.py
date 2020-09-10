#!/usr/bin/python3
"""This module is in charge of handling requests for state-type objects."""
from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.city import City
from flask import abort
from flask import make_response
from flask import request
from models.state import State


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['GET'])
def get_cities(state_id):
    """return all city in states id"""
    if state_id:
        dict_state = storage.get(State, state_id)
        if dict_state is None:
            abort(404)
        else:
            cities = storage.all(City).values()
            list_cities = []
            for city in cities:
                if city.state_id == state_id:
                    list_cities.append(city.to_dict())
            return jsonify(list_cities)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """Get a specific City object through the HTTP GET request"""
    if city_id:
        dict_city = storage.get(City, city_id)
        if dict_city is None:
            abort(404)
        else:
            return jsonify(dict_city.to_dict())


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """Delete a specific City object through the HTTP DELETE request"""
    if city_id:
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        else:
            storage.delete(city)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('states/<state_id>/cities',
                 strict_slashes=False, methods=['POST'])
def response_city(state_id):
    """Create a new City object through the HTTP POST request"""
    if state_id:
        state = storage.get(State, state_id)
        if state is None:
            abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    req = request.get_json()
    if "name" not in req:
        return make_response(jsonify({"error": "Missing name"}), 400)
    req['state_id'] = state_id
    city = City(**req)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """Update a specific City object through the HTTP PUT request"""
    if city_id:
        obj_cities = storage.get(City, city_id)
        if obj_cities is None:
            abort(404)

        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        req = request.get_json()
        for key, value in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(obj_cities, key, value)
        obj_cities.save()
        return make_response(jsonify(obj_cities.to_dict()), 200)
