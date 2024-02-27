#!/usr/bin/python3
"""
creates a new view for city objects, will handle all
default RESTful API actions
"""

#importing the necessary modules
from models.base_model import BaseModel
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id):
    """
    lists all city objects found in a state
    """
    output_list = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        for city in state.cities:
            output_list.append(city.to_dict())
        return (jsonify(output_list))
    if request.method == 'POST':
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        if 'name' not in request.json:
            abort(400, description="Missing name")
        user_data['state_id'] = state_id
        city = City(**user_data)
        city.save()
        return (jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['GET', 'PUT'],
                 strict_slashes=False)
def ID_city(city_id):
    """
    lists a city in order of iD
    """
    defined_city = storage.get(City, city_id)
    if defined_city is None:
        abort(404)
    if request.method == 'GET':
        user_output = defined_city.to_dict()
        return (jsonify(user_output))
    if request.method == 'PUT':
        user_data = request.get_json()
        if not request.is_json:
            abort(400, description="Not a JSON")
        for key, value in user_data.items():
            setattr(defined_city, key, value)
        defined_city.save()
        return (jsonify(defined_city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=["GET", "DELETE"],
                 strict_slashes=False)
def del_a_city(city_id):
    """
    delete one unique city object
    """
    defined_city = storage.get(City, city_id)
    if defined_city is None:
        abort(404)
    storage.delete(defined_city)
    storage.save()
    result = make_response(jsonify({}), 200)
    return result
