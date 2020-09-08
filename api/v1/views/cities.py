#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, Blueprint, make_response, abort
from models import storage
from models.city import City
from models.state import State
from models.base_model import BaseModel


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """list all cities in state"""
    output = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        output.append(city.to_dict())
    return (jsonify(output))


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def a_city(city_id):
    """list a city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    output = city.to_dict()
    return (jsonify(output))


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
