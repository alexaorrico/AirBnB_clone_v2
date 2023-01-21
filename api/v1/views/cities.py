#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.city import City
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id):
    """list all cities in state"""
    output = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        for city in state.cities:
            output.append(city.to_dict())
        return (jsonify(output))
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


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def a_city(city_id):
    """list a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        output = city.to_dict()
        return (jsonify(output))
    if request.method == 'PUT':
        data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in data.items():
            setattr(city, key, value)
        city.save()
        return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_a_city(city_id):
    """ delete one unique city object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
