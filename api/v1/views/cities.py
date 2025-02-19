#!/usr/bin/python3
"""Cities file that contains API routes related to city object operation"""

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, make_response, request, jsonify


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=["GET"])
def get_cities_by_state_id(state_id=None):
    """ Find cities by state id"""
    cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        allCities = storage.all(City).values()
        for c in allCities:
            if c.state_id == state_id:
                cities.append(c.to_dict())
    return jsonify(cities)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["GET"])
def get_city_by_id(city_id=None):
    """ Find a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["DELETE"])
def delete_city_by_id(city_id=None):
    """ Delete a city by ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=["POST"])
def create_city(state_id=None):
    """ Creates a city in a state"""
    data = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=["PUT"])
def update_city(city_id=None):
    """ Update city data"""
    data = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in data.items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)
    city.save()
    return jsonify(city.to_dict())
