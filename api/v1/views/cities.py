#!/usr/bin/python3
"""Creating state objects to handle all default RESTFUL APIs"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from api.v1.views import app_views
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities', methods=["GET", "POST"],
                 strict_slashes=False)
def cities_in_state(state_id):
    """Getting all cities within a state"""
    all_cities = []
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if request.method == "GET":
        for city in state.cities:
            all_cities.append(city.to_dict())
        return (jsonify(all_cities))

    if request.method == 'POST':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=["GET", "PUT"],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieve city by id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if request.methods == "GET":
        result = city.to_dict()
        return (jsonify(result))

    if request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(city, key, value)
        city.save()
        return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["DELETE"],
                 strict_slashes=False)
def del_cities(city_id):
    """Delete a city by it's id"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        new_cities = make_response(jsonify({}), 200)
        return new_cities
